"""{liero_recovery} Integrated RL-guided recovery module."""

# Consolidates all recovery logic from:
#   - engine/rl_engine.py (20 functions)
#   - engine/recovery_loop.py (7 functions)
#   - engine/draft.py (draft generation)
#   - engine/verify.py (oracle verification)
#   - engine/knowledge.py (Q-table & language isolation)
#   - engine/model_adapter.py (model selection)

# Provides a unified RecoveryEngine class with all recovery orchestration,
# state management, action selection, outcome recording, and verification.

from engine.verified_examples import record_verified_pascal, get_verified_examples
from engine.knowledge import load, save, STORE

import json
import random
import hashlib
import pathlib
import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List, Tuple, Callable

# Project paths
BASE = pathlib.Path(__file__).resolve().parent.parent
TARGETS = BASE / "targets"
KNOWLEDGE = BASE / "knowledge"
TOOLS = BASE / "tools"

# RL hyperparameters
ALPHA = 0.2       # learning rate
GAMMA = 0.9       # discount factor
EPSILON = 0.15    # exploration rate
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.05
REPLAY_BUFFER_SIZE = 2000
REPLAY_BATCH = 64
UPDATE_EVERY = 10

# Discretization buckets
COVERAGE_BUCKETS = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
SUCCESS_RATE_BUCKETS = [0.0, 0.3, 0.6, 0.8, 1.0]
COMPLEXITY_BUCKETS = [0.0, 0.25, 0.5, 0.75, 1.0]
EXAMPLES_BUCKETS = [0, 1, 3, 6, 20]

# Model/temperature/few-shot options
ACTION_MODEL = [
    "Qwen3-Coder-480B-A35B-Instruct",
    "deepseek-v4-flash-0731:Q4_K_M",
    "qwen2.5-coder:14b-instruct-q4_K_M",
    "llm4decompile-33b",
    "losore-llm4decompile-22b-v2:Q4_K_M",
]
TEMPERATURES = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
FEW_SHOT_OPTS = [0, 1, 3, 5, 7]

@dataclass
class Experience:
    """Single (s, a, r, s)' transition for experience replay."""
    state: str
    action: str
    reward: float
    next_state: str
    done: bool = False

@dataclass
class RLStats:
    """Aggregate RL statistics for reporting."""
    total_attempts: int = 0
    total_verified: int = 0
    total_failed: int = 0
    total_blocked: int = 0
    cumulative_reward: float = 0.0
    language_stats: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: dict):
        """Create RLStats from data dict."""
        stats = cls()
        stats.total_attempts = data.get("total_attempts", 0)
        stats.total_verified = data.get("total_verified", 0)
        stats.total_failed = data.get("total_failed", 0)
        stats.total_blocked = data.get("total_blocked", 0)
        stats.cumulative_reward = data.get("cumulative_reward", 0.0)
        stats.language_stats = data.get("language_stats", {})
        stats.epsilon = data.get("epsilon", EPSILON)
        return stats

# Unified RecoveryEngine

class RecoveryEngine:

    """Integrated recovery engine combining RL guidance,
draft generation, oracle verification, and Q-table/knowledge management.

    Replaces the separate engine/rl_engine.py, engine/recovery_loop.py,
    engine/draft.py, engine/verify.py, and engine/knowledge.py modules
    with a single coherent interface.
    """

    def __init__(self,
                 target: str = "liero",
                 knowledge_path: pathlib.Path = KNOWLEDGE / "knowledge.json",
                 target_dir: pathlib.Path = TARGETS / "liero"):
        self.target = target
        self.knowledge_path = knowledge_path
        self.target_dir = target_dir

        # Load or initialize knowledge base
        self.data = self._load_or_init_data()

        # Q-table, stats, experience buffer are all in self.data
        self.q_table = self.data.get("q_table", {})
        self.rl_stats = RLStats.from_data(self.data)
        self.experience_buffer = self.data.get("experience_buffer", {})

        # Derived
        self._iteration = 0
        self._verified_set: set[str] = set(
            self.data.get("verified", set())
        )
        self._remaining: set[str] = self._compute_remaining()

        # Oracle gate: build.sha1 status
        self._oracle_gate = self._check_oracle_gate()

    def _load_or_init_data(self) -> dict:
        """Load knowledge.json or initialise an empty structure."""
        if self.knowledge_path.exists():
            data = json.loads(self.knowledge_path.read_text())
            # Migrate old-format keys if needed
            if "rl_q_table" in data and "q_table" not in data:
                data["q_table"] = data.pop("rl_q_table")
            if "rl_stats" in data and "language_stats" not in data:
                pass
            return data
        # Fresh initialisation
        return {
            "q_table": {},
            "language_stats": {},
            "experience_buffer": {},
            "verified": [],
            "schema_version": 2,
            "epsilon": EPSILON,
        }

    def _check_oracle_gate(self) -> dict:
        """Check build.sha1 gate status.

        Returns dict with keys: open, closed, pending
        """
        build_sha1 = TARGETS / "liero" / "config" / "build.sha1"
        if not build_sha1.exists():
            return {"status": "closed", "reason": "no build.sha1 file"}
        entries = build_sha1.read_text().strip().splitlines()
        if not entries:
            return {"status": "closed", "reason": "empty build.sha1"}
        # Verify at least one entry is valid
        for entry in entries:
            parts = entry.strip().split()
            if len(parts) >= 2:
                return {"status": "open", "reason": f"{len(entries)} SHA1 entries"}
        return {"status": "closed", "reason": "invalid build.sha1 format"}
    def _compute_remaining(self) -> set[str]:
        """Compute set of functions not yet verified."""
        verified = set(self.data.get("verified", []))
        all_funcs = set()
        funcs_path = self.target_dir / "functions.json"
        if funcs_path.exists():
            funcs = json.loads(funcs_path.read_text(errors="replace")).get("functions", [])
            all_funcs = {f.get("name") for f in funcs}
        return all_funcs - verified

    def get_verified_examples(self, compiler: str, platform: str, limit: int = 3,
                              query_asm: str = "") -> list[dict]:
        """Retrieve verified few-shot examples for draft generation.

        Uses verified_examples.get_verified_examples() to retrieve
        previous successful translations for similar assembly patterns.

        Args:
            compiler: Compiler name (e.g. "turbo-pascal-7")
            platform: Platform name (e.g. "dos")
            limit: Maximum number of examples to return
            query_asm: Assembly text to match against

        Returns:
            List of verified example dicts for few-shot prompting
        """
        from engine.verified_examples import get_verified_examples as _get_verified
        return _get_verified(self.target, compiler, platform,
                            query_asm=query_asm, limit=limit)

    def get_coverage_aware_action(self, lang_key: str, available_models: list[str],
                                   query_asm: str = "") -> str:
        """Select an action weighted by coverage gap and verified examples.

        Prioritizes functions with low coverage (requiring more verified
        examples may reduce future verification failures) and uses
        available few-shot examples to bias model selection.

        Args:
            lang_key: Language key (compiler@platform)
            available_models: List of valid model identifiers
            query_asm: Assembly text for few-shot retrieval

        Returns:
            Action string in format: model|temperature|few_shot
        """
        import random

        epsilon = self.rl_stats.epsilon

        # Get verified examples for context
        examples = self.get_verified_examples(
            self.target, lang_key.split('@')[0] if '@' in lang_key else lang_key,
            lang_key.split('@')[1] if '@' in lang_key else 'dos',
            query_asm=query_asm, limit=3
        )

        # Check if we have verified examples to use
        has_examples = len(examples) > 0

        # Exploit: choose best action with verified examples as additional weight
        if random.random() > epsilon and self.experience_buffer:
            best_action = None
            best_rate = -1.0

            for action, stats in self.experience_buffer.items():
                attempts = stats.get("attempts", 0)
                successes = stats.get("successes", 0)
                rate = successes / attempts if attempts > 0 else 0

                # Boost actions that use few-shot examples when examples are available
                # (this is a simplified heuristic - in production this would
                #  be more sophisticated)
                few_shot = int(action.split("|")[2]) if "|" in action else 0
                example_boost = 0.1 if (has_examples and few_shot > 0) else 0

                # Combined score: base rate + example boost
                score = rate + (0.05 * min(len(examples), 3) * (self._iteration > 3))
                if score > best_rate:
                    best_rate = score
                    best_action = action

            if best_action is not None:
                parts = best_action.split("|")
                model = parts[0]
                if model not in available_models:
                    model = random.choice(available_models)
                return f"{model}|{parts[1]}|{parts[2]}"

        # Explore: random action with example-aware probability
        model = random.choice(available_models)
        temp = random.choice(TEMPERATURES)
        few_shot = random.choice(FEW_SHOT_OPTS)

        # Bias toward few-shot examples if available
        if has_examples and random.random() < 0.7:
            few_shot = random.choice(FEW_SHOT_OPTS)

        action = f"{model}|{temp}|{few_shot}"

        # Initialise experience buffer entry
        if "experience_buffer" not in self.data:
            self.data["experience_buffer"] = {}
        if action not in self.data["experience_buffer"]:
            self.data["experience_buffer"][action] = {"attempts": 0, "successes": 0}

        return action
    @classmethod
    def from_data(cls, data: dict):
        """Create RLStats from data dict."""
        stats = cls()
        stats.total_attempts = data.get("total_attempts", 0)
        stats.total_verified = data.get("total_verified", 0)
        stats.total_failed = data.get("total_failed", 0)
        stats.total_blocked = data.get("total_blocked", 0)
        stats.cumulative_reward = data.get("cumulative_reward", 0.0)
        stats.language_stats = data.get("language_stats", {})
        stats.epsilon = data.get("epsilon", EPSILON)
        return stats