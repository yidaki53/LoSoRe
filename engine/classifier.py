
"""Software classifier: determines type, language, and purpose of a target."""

from __future__ import annotations
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


def detect_software_type(target: str) -> str:
    """
    Detect the type of software for a given target.
    
    Returns one of: "game", "driver", "utility", "unknown"
    Based on the 'kind' field in target config, with fallback analysis.
    """
    target_dir = pathlib.Path(target)
    config_path = target_dir / "config" / "target.yaml"
    if config_path.exists():
        with open(config_path) as f:
            content = f.read()
        if "kind: game" in content:
            return "game"
        elif "kind: driver" in content:
            return "driver"
        elif "kind: utility" in content:
            return "utility"
    # Fallback: analyze functions.json if available
    functions_path = target_dir / "functions.json"
    if functions_path.exists():
        with open(functions_path) as f:
            data = json.load(f)
        # Check function names for clues
        funcs = data.get("functions", [])
        if funcs:
            # If functions have game-related names or patterns
            game_keywords = ['fire', 'shoot', 'player', 'enemy', 'npc', 'ai', 'weapon', 'explos']
            names = [fn.get("name", "").lower() for fn in funcs]
            if any(kw in name for name in names for kw in game_keywords):
                return "game"
    return "unknown"


def detect_language(target: str) -> str:
    """
    Detect the source code language for a given target.
    
    Returns language string or 'unknown'
    Based on target config or functions.json metadata.
    """
    target_dir = pathlib.Path(target)
    config_path = target_dir / "config" / "target.yaml"
    if config_path.exists():
        with open(config_path) as f:
            content = f.read()
        if "language: pascal" in content:
            return "pascal"
        elif "language: c" in content:
            return "c"
        elif "language: cpp" in content:
            return "cpp"
        elif "language: asm" in content:
            return "asm"
    # Fallback: functions.json metadata
    functions_path = target_dir / "functions.json"
    if functions_path.exists():
        with open(functions_path) as f:
            data = json.load(f)
        lang = data.get("language", "")
        if lang:
            return lang
    return "unknown"


def detect_purpose(target: str) -> str:
    """
    Detect the purpose/category of a target software.
    
    Returns purpose description based on function analysis.
    """
    kind = detect_software_type(target)
    if kind == "game":
        # Analyze function names for game subsystems
        functions_path = pathlib.Path(target) / "functions.json"
        if functions_path.exists():
            with open(functions_path) as f:
                data = json.load(f)
            funcs = data.get("functions", [])
            subsystems = {
                'movement': any('mov' in fn.get("name", "").lower() for fn in funcs),
                'shooting': any(s in fn.get("name", "").lower() for fn in funcs for s in ['shot', 'bullet', 'fire']),
                'ai': any('ai' in fn.get("name", "").lower() or 'npc' in fn.get("name", "").lower() for fn in funcs),
                'physics': any('phys' in fn.get("name", "").lower() for fn in funcs),
                'level': any('level' in fn.get("name", "").lower() for fn in funcs),
                'particles': any('part' in fn.get("name", "").lower() for fn in funcs),
                'utility': any('util' in fn.get("name", "").lower() for fn in funcs),
            }
            detected = [k for k, v in subsystems.items() if v]
            if detected:
                return f"game ({', '.join(detected)})"
        return "game"
    elif kind == "driver":
        return "driver/utility"
    elif kind == "utility":
        return "utility"
    return "unknown"


def get_oracle_for_type(software_type: str, target: str, data: dict | None = None) -> str:
    """
    Select appropriate oracle based on software type.
    
    For games: prefer dat-parity if DAT available, else byte-exact
    For drivers: use byte-exact or relocation-aware
    For other: default to byte-exact
    """
    from engine.oracle_recommender import recommend_oracle
    
    target_dir = pathlib.Path(target)
    if software_type == "game":
        # Games prefer dat-parity if DISC image available
        dat_oracle = target_dir / "tools" / "liero_dat.py"
        if dat_oracle.exists():
            return "dat-parity"
        # Also check knowledge base for similar toolchains
        if data is None:
            data = knowledge.load() if pathlib.Path("knowledge/knowledge.json").exists() else {}
        rec = recommend_oracle(target, "unknown", "unknown", data)
        if rec in ["byte-exact", "relocation-aware", "round-trip", "trace-parity", "dat-parity"]:
            return rec
        return "byte-exact"
    elif software_type == "driver":
        return "byte-exact"
    else:
        return "byte-exact"


def get_rl_config(software_type: str, coverage: float = 0.0, verified_count: int = 0, total_count: int = 0) -> dict:
    """
    Get RL configuration based on software type.
    """
    base_config = {
        "alpha": 0.2,
        "gamma": 0.9,
        "epsilon": 0.15,
        "epsilon_decay": 0.995,
        "epsilon_min": 0.05,
    }
    
    if software_type == "game":
        # Game-specific: coverage-aware, subsystem-aware
        base_config["subsystem_weights"] = {
            "movement": 1.0,
            "shooting": 0.9,
            "ai": 0.8,
            "physics": 0.7,
            "level": 0.5,
            "particles": 0.3,
            "utility": 0.1,
        }
        base_config["coverage_reward_multiplier"] = 0.1
        base_config["example_boost_factor"] = 0.1
    elif software_type == "driver":
        # Driver-specific: simpler, less exploration
        base_config["epsilon"] = 0.05  # Less exploration
        base_config["epsilon_decay"] = 0.99  # Faster decay
        base_config["subsystem_weights"] = {
            "main": 1.0,
        }
    else:
        # Other software: minimal RL
        base_config["epsilon"] = 0.01
        base_config["gamma"] = 0.5
    
    return base_config


# Export main functions
__all__ = [
    "detect_software_type",
    "detect_language",
    "detect_purpose",
    "get_oracle_for_type",
    "get_rl_config",
]
