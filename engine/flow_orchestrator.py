
"""Flow orchestrator: flexible flowchart for agnostic software learning.

Determines source code language, type of software, purpose of software,
and then does the appropriate oracle, RL, and DL based on that.
"""

from __future__ import annotations
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from engine.classifier import (
    detect_software_type,
    detect_language,
    detect_purpose,
    get_oracle_for_type,
    get_rl_config,
)

import knowledge


def run_flowchart(target: str) -> dict:
    """
    Run the complete flexible flowchart for a target.

    The flowchart:
    1. Determines source code language
    2. Determines type of software (game vs other)
    3. Determines purpose of software
    4. Selects appropriate oracle based on type
    5. Selects RL configuration based on type
    6. Returns flow summary and recommendations
    """
    # Step 1: Determine source code language
    language = detect_language(target)

    # Step 2: Determine type of software
    software_type = detect_software_type(target)

    # Step 3: Determine purpose of software
    purpose = detect_purpose(target)

    # Step 4: Select appropriate oracle based on type
    data = knowledge.load() if pathlib.Path("knowledge/knowledge.json").exists() else None
    oracle = get_oracle_for_type(software_type, target, data)

    # Step 5: Select RL configuration based on type
    coverage = 0.0  # Would be computed from existing knowledge base
    verified_count = 0  # Would be computed from existing knowledge base
    total_count = 295  # Total functions in target
    rl_config = get_rl_config(software_type, coverage, verified_count, total_count)

    # Step 6: Additional DL/model selection based on software type
    model_selection = select_dl_model(software_type, language, rl_config)

    # Compile flow summary
    flow_summary = {
        "target": target,
        "software_type": software_type,
        "language": language,
        "purpose": purpose,
        "oracle": oracle,
        "rl_config": rl_config,
        "dl_model": model_selection,
        "flow_steps": [
            {"step": 1, "action": f"Detect language: {language}"},
            {"step": 2, "action": f"Detect software type: {software_type}"},
            {"step": 3, "action": f"Detect purpose: {purpose}"},
            {"step": 4, "action": f"Select oracle: {oracle}"},
            {"step": 5, "action": f"Select RL config: alpha={rl_config['alpha']}, epsilon={rl_config['epsilon']}"},
            {"step": 6, "action": f"Select DL model: {model_selection['model']}"},
        ]
    }

    return {
        "flow_summary": flow_summary,
        "software_type": software_type,
        "language": language,
        "purpose": purpose,
        "oracle": oracle,
        "rl_config": rl_config,
        "dl_model": model_selection,
    }


def select_dl_model(software_type: str, language: str, rl_config: dict) -> dict:
    """
    Select appropriate Deep Learning model and parameters based on software type.

    For games: select models capable of learning state transitions and AI behaviors
    For drivers: select simpler models focused on deterministic patterns
    For other: select general-purpose models
    """
    available_models = [
        "Qwen3-Coder-480B-A35B-Instruct",
        "deepseek-v4-flash-0731:Q4_K_M",
        "qwen2.5-coder:14b-instruct-q4_K_M",
        "llm4decompile-33b",
        "losore-llm4decompile-22b-v2:Q4_K_M",
    ]

    if software_type == "game":
        # For games, select models capable of learning state transitions
        # and AI behaviors, with temperature tuned for creativity
        model = available_models[0]  # Qwen3-Coder (best for code/game decompilation)
        temp = 0.5  # Balanced temperature for game state learning
        few_shot = 3  # Use few-shot examples from verified functions
        return {
            "model": model,
            "temperature": temp,
            "few_shot": few_shot,
            "description": "Game decompilation model with few-shot for state transitions"
        }
    elif software_type == "driver":
        # For drivers, select simpler model with lower temperature
        model = available_models[4]  # losore-llm4decompile (good for driver analysis)
        temp = 0.3  # Lower temperature for deterministic driver analysis
        few_shot = 1  # Minimal few-shot
        return {
            "model": model,
            "temperature": temp,
            "few_shot": few_shot,
            "description": "Driver analysis model with minimal few-shot"
        }
    else:
        # For other software, use general-purpose configuration
        model = available_models[2]  # qwen2.5-coder
        temp = 0.7  # Higher temperature for exploration
        few_shot = 0  # No few-shot unless available
        return {
            "model": model,
            "temperature": temp,
            "few_shot": few_shot,
            "description": "General-purpose decompilation model"
        }


def run_verification_with_flow(target: str, priority_fns: list | None = None, oracle: str | None = None) -> dict:
    """
    Run verification integrated with the flowchart flow.

    This integrates the flowchart determination with the verification loop,
    ensuring the correct oracle and RL/DL configuration is used.
    """
    # Run flowchart to determine parameters
    flow_result = run_flowchart(target)

    # Use flowchart-determined oracle if not provided
    if oracle is None:
        oracle = flow_result["oracle"]

    # Use flowchart-determined RL config
    rl_config = flow_result["rl_config"]

    # Determine if we should proceed with verification based on software type
    if flow_result["software_type"] == "driver":
        # For drivers, use byte-exact oracle with relocation-aware as fallback
        pass  # Already determined above

    # Return the complete flow result along with verification parameters
    return {
        "flow_result": flow_result,
        "oracle": oracle,
        "rl_config": rl_config,
        "target": target,
    }


# Export main functions
__all__ = [
    "run_flowchart",
    "select_dl_model",
    "run_verification_with_flow",
]
