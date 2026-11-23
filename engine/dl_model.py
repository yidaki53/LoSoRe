"""Deep Learning model for code generation - puzzle-solving inspired code refinement.

Provides a conditional GPT-2 generator that takes function metadata and produces
Pascal function bodies. Inspired by puzzle-solving: iteratively refines code based
on previously "solved" (verified) fragments.

Supports training from multiple sources:
- Liero verified functions (primary)
- Other Pascal code collections (supplementary)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tarfile
import torch
from pathlib import Path
from typing import Dict, List, Optional

import torch.nn as nn
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.utils.data import Dataset, DataLoader


MODEL_DIR = Path(__file__).resolve().parent.parent / "model_weights"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def _is_pascal_file(filename: str) -> bool:
    """Check if a file is a Pascal source file (case-insensitive)."""
    return filename.lower().endswith((".pas", ".p", ".pp"))


def _pad_collate(batch):
    """Custom collate function that pads tensors in a batch to the same length."""
    # Separate input_ids and labels
    input_ids = [item["input_ids"] for item in batch]
    labels = [item["labels"] for item in batch]
    
    # Pad input_ids to the same length within the batch
    input_ids_padded = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=0)
    labels_padded = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=-100)  # -100 is ignored in loss
    
    return {"input_ids": input_ids_padded, "labels": labels_padded}


def _load_verified_examples(target: str, oracle: str) -> List[Dict[str, str]]:
    """Load verified Pascal examples from the knowledge base.

    Args:
        target: Target slug (e.g. "liero")
        oracle: Oracle that verified the functions

    Returns:
        List of dicts with 'fn' and 'pascal' keys
    """
    from engine.knowledge import load, STORE
    from engine.verified_examples import compiler_key

    data = load(STORE)
    examples: List[Dict[str, str]] = []

    compilers = data.get("compilers", {})
    key = None
    for k in compilers.keys():
        key = k
        break

    if key is None:
        print("No compiler key found in knowledge store")
        return examples

    stored_examples = data.get("verified_pascal_examples", {}).get(key, [])

    for ex in stored_examples:
        if ex.get("oracle") == oracle and ex.get("verification_status") == "verified":
            pascal = ex.get("pascal", "")
            examples.append({"fn": ex.get("fn", ""), "pascal": pascal})

    return examples


def _load_pascal_from_collection(collection_path: Path, limit: int = None) -> List[Dict[str, str]]:
    """Load Pascal source files from a collection directory.

    Args:
        collection_path: Path to directory containing .pas files
        limit: Maximum number of files to load (None for all)

    Returns:
        List of dicts with 'fn' and 'pascal' keys
    """
    examples: List[Dict[str, str]] = []

    pascal_files = []
    for root, dirs, files in os.walk(collection_path):
        for f in files:
            if _is_pascal_file(f):
                pascal_files.append(os.path.join(root, f))

    pascal_files.sort()

    for i, pascal_file in enumerate(pascal_files):
        if limit is not None and i >= limit:
            break

        try:
            with open(pascal_file, "r", errors="replace") as f:
                pascal_body = f.read()

            # Extract function name from the Pascal file
            # Look for 'function Name...' or 'procedure Name...'
            name_match = re.search(r"(?:procedure|function)\s+(\w+)", pascal_body)
            fn_name = name_match.group(1) if name_match else os.path.splitext(os.path.basename(pascal_file))[0]

            examples.append({
                "fn": fn_name,
                "pascal": pascal_body,
            })
        except Exception as e:
            print(f"Error loading {pascal_file}: {e}")
            continue

    return examples


def _load_pascal_from_tar(tar_path: Path, limit: int = None) -> List[Dict[str, str]]:
    """Load Pascal source files from a .tar.gz archive.

    Args:
        tar_path: Path to .tar.gz file
        limit: Maximum number of files to load

    Returns:
        List of dicts with 'fn' and 'pascal' keys
    """
    examples: List[Dict[str, str]] = []

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            pascal_members = [m for m in tar.getmembers() if _is_pascal_file(os.path.basename(m.name))]
            pascal_members.sort(key=lambda m: m.name)

            for i, member in enumerate(pascal_members):
                if limit is not None and i >= limit:
                    break

                try:
                    f = tar.extractfile(member)
                    if f is None:
                        continue

                    pascal_body = f.read().decode("latin-1", errors="replace")

                    # Extract function name
                    name_match = re.search(r"(?:procedure|function)\s+(\w+)", pascal_body)
                    fn_name = name_match.group(1) if name_match else os.path.splitext(member.name)[0]

                    examples.append({
                        "fn": fn_name,
                        "pascal": pascal_body,
                    })
                except Exception as e:
                    print(f"Error extracting {member.name}: {e}")
                    continue
    except Exception as e:
        print(f"Error opening tar {tar_path}: {e}")

    return examples


class FunctionMetadataEncoder(nn.Module):
    """Encodes function metadata into a context vector for conditioning the generator."""

    def __init__(self, num_categories: int = 100):
        super().__init__()
        self.num_categories = num_categories
        self.name_embedding = nn.Embedding(num_categories, 32)
        self.cc_embedding = nn.Embedding(num_categories, 16)
        self.subsystem_embedding = nn.Embedding(num_categories, 16)
        self.size_embedding = nn.Embedding(num_categories, 8)

    def forward(self, metadata: Dict[str, Any]) -> torch.Tensor:
        name_hash = int(hashlib.md5(metadata.get("name", "unknown").encode()).hexdigest(), 16) % self.num_categories
        cc_hash = int(hashlib.md5(metadata.get("calling_convention", "unknown").encode()).hexdigest(), 16) % self.num_categories
        subsystem_hash = int(hashlib.md5(metadata.get("subsystem", "unknown").encode()).hexdigest(), 16) % self.num_categories
        size_hash = int(hashlib.md5(str(metadata.get("size", 0)).encode()).hexdigest(), 16) % self.num_categories

        name_emb = self.name_embedding(torch.tensor(name_hash, dtype=torch.long))
        cc_emb = self.cc_embedding(torch.tensor(cc_hash, dtype=torch.long))
        subsystem_emb = self.subsystem_embedding(torch.tensor(subsystem_hash, dtype=torch.long))
        size_emb = self.size_embedding(torch.tensor(size_hash, dtype=torch.long))

        return torch.cat([name_emb, cc_emb, subsystem_emb, size_emb])


class DLFunctionGenerator:
    """Conditional GPT-2 generator for Pascal function bodies."""

    def __init__(self, model_name: str = "gpt2"):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.metadata_encoder = FunctionMetadataEncoder()

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.model.config.eos_token_id

        # Input dim is sum of embedding sizes: 32 + 16 + 16 + 8 = 72
        self.metadata_projection = nn.Linear(72, self.model.config.n_embd)

    def predict(
        self,
        metadata: Dict[str, Any],
        max_length: int = 128,
        temperature: float = 0.7,
        do_sample: bool = True,
    ) -> str:
        """Generate a Pascal function body given function metadata.

        Args:
            metadata: Dict with keys: name, calling_convention, subsystem, size
            max_length: Maximum tokens to generate
            temperature: Sampling temperature
            do_sample: Whether to use sampling

        Returns:
            Generated Pascal function body text
        """
        context_vec = self.metadata_encoder(metadata)
        context_vec = context_vec.unsqueeze(0)
        projected = self.metadata_projection(context_vec)

        input_ids = torch.tensor([[self.tokenizer.eos_token_id]], dtype=torch.long)

        output = self.model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            do_sample=do_sample,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def save_pretrained(self, path: Path = None) -> None:
        if path is None:
            path = MODEL_DIR / "generator"
        path.mkdir(parents=True, exist_ok=True)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        torch.save(self.metadata_encoder.state_dict(), path / "metadata_encoder.pt")

    @classmethod
    def load_pretrained(cls, path: Path = None) -> "DLFunctionGenerator":
        if path is None:
            path = MODEL_DIR / "generator"
        instance = cls()
        instance.model = GPT2LMHeadModel.from_pretrained(str(path))
        instance.tokenizer = GPT2Tokenizer.from_pretrained(str(path))
        if (path / "metadata_encoder.pt").exists():
            instance.metadata_encoder.load_state_dict(torch.load(path / "metadata_encoder.pt"))
        return instance


def train_incremental(
    model: DLFunctionGenerator,
    target: str = "liero",
    oracle: str = "dat-parity",
    epochs: int = 1,
    batch_size: int = 4,
    supplement_collections: List[Path] = None,
) -> Dict[str, float]:
    """Incrementally train the model on newly verified examples.

    Args:
        model: DLFunctionGenerator instance (will be updated in place)
        target: Target slug
        oracle: Oracle that verified the functions
        epochs: Number of training epochs
        batch_size: Training batch size
        supplement_collections: List of paths to Pascal code collections for supplementary training

    Returns:
        Training metrics (loss, etc.)
    """
    from torch.utils.data import DataLoader

    # Load primary verified examples
    examples = _load_verified_examples(target, oracle)
    print(f"Loaded {len(examples)} verified examples for training")

    # Load supplementary Pascal code if requested
    all_pascal_texts = list(ex["pascal"] for ex in examples) if examples else []

    if supplement_collections:
        print(f"Loading {len(supplement_collections)} Pascal collections for supplementary training...")
        for collection_path in supplement_collections:
            if collection_path.exists():
                coll_examples = _load_pascal_from_collection(collection_path, limit=50)
                coll_texts = [ex["pascal"] for ex in coll_examples]
                all_pascal_texts.extend(coll_texts)
                print(f"  Loaded {len(coll_texts)} Pascal bodies from {collection_path.name}")
            else:
                print(f"  Collection not found: {collection_path}")
    
    if not all_pascal_texts:
        print("No Pascal texts to train on - skipping training")
        return {"loss": float("nan")}

    print(f"Total Pascal texts: {len(all_pascal_texts)}")

    class PascalDataset(Dataset):
        def __init__(self, texts: List[str], tokenizer, max_length: int = 128):
            self.texts = texts
            self.tokenizer = tokenizer
            self.max_length = max_length

        def __len__(self):
            return len(self.texts)

        def __getitem__(self, idx):
            text = self.texts[idx]
            tokens = self.tokenizer(
                text,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt",
                padding="max_length",
            )
            input_ids = tokens.input_ids.squeeze(0)
            labels = input_ids.clone()
            return {"input_ids": input_ids, "labels": labels}

    dataset = PascalDataset(all_pascal_texts, model.tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=_pad_collate)

    model.model.train()
    optimizer = torch.optim.AdamW(model.model.parameters(), lr=1e-5)
    total_loss = 0.0
    num_batches = 0

    for epoch in range(epochs):
        for batch in dataloader:
            input_ids = batch["input_ids"]
            labels = batch["labels"]

            outputs = model.model(input_ids=input_ids, labels=labels)
            loss = outputs.loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1

    avg_loss = total_loss / max(num_batches, 1)
    print(f"Training complete. Average loss: {avg_loss:.4f}")

    model.save_pretrained()

    return {"loss": avg_loss}


def generate_prompted(
    model: DLFunctionGenerator,
    metadata: Dict[str, str],
    examples: List[Dict[str, str]],
    max_length: int = 256,
) -> str:
    """Generate a Pascal function body using few-shot prompting.

    Args:
        model: DLFunctionGenerator instance
        metadata: Function metadata dict
        examples: List of (fn, pascal) few-shot examples
        max_length: Maximum tokens to generate

    Returns:
        Generated Pascal function body
    """
    tokenizer = model.tokenizer

    prompt_parts: List[str] = []
    for ex in examples[:3]:
        body = ex["pascal"]
        if len(body) > 200:
            body = body[:200] + "..."
        prompt_parts.append(f"Function: {ex['fn']}\nPascal:\n{body}\n")

    prompt_parts.append(f"Function: {metadata.get('name', 'UNKNOWN')}\nPascal:\n")

    prompt = "\n".join(prompt_parts)

    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    output = model.model.generate(
        input_ids,
        max_new_tokens=max_length,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    print("DL Function Generator - Puzzle Solver Model")
    print("=" * 50)

    generator = DLFunctionGenerator()

    example_metadata = {
        "name": "FUN_1000_01a1",
        "calling_convention": "__cdecl16near",
        "subsystem": "movement",
        "size": 32,
    }

    print("\nGenerating draft function body (random, before training)...")
    draft = generator.predict(example_metadata, max_length=64, temperature=0.8)
    print(f"Generated draft (first 200 chars):")
    print(draft[:200])

    generator.save_pretrained()
    print("\nInitial model saved. Ready for incremental training on verified examples.")
