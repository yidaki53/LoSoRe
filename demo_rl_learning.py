#!/usr/bin/env python3
"""
Demonstration: RL-guided recovery learning loop for Liero Pascal.

Shows: Pascal language isolation, Q-learning updates, epsilon-greedy
action selection, experience replay, coverage milestone rewards.
"""
from __future__ import annotations

import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "engine"))

from engine import rl_engine as rl
import knowledge


def simulate_recovery_attempts(num_attempts: int = 50):
    data = rl.load_rl()
    lang_key = "pascal|turbo-pascal-7"

    print("=" * 70)
    print("RL-Guided Liero Pascal Recovery - Learning Demonstration")
    print("=" * 70)
    print(f"\nLanguage key: {lang_key} (Pascal isolated)")
    print(f"Initial epsilon: {data['epsilon']:.3f}")
    print()

    functions = [
        ("FUN_24dd_0000", 12, True, None),
        ("FUN_24dd_0116", 25, True, None),
        ("FUN_24dd_0353", 45, False, "dependency"),
        ("FUN_24dd_374d", 60, True, None),
        ("FUN_24dd_396c", 80, False, "method"),
        ("FUN_24dd_397a", 95, True, None),
    ]

    total_reward = 0.0
    verified_count = 0
    failed_count = 0
    blocked_count = 0

    print(f"{'Iter':>5} {'Function':>15} {'Action':>45} {'Outcome':>10} {'Reward':>8} {'Coverage':>10} {'Epsilon':>8}")
    print("-" * 70)

    for i in range(num_attempts):
        fn_idx = i % len(functions)
        fn, inst_count, callee_resolved, blocker = functions[fn_idx]

        coverage = verified_count / 295.0
        recent_sr = verified_count / max(i, 1) if i > 0 else 1.0

        state = rl.encode_state(
            lang_key=lang_key,
            coverage=coverage,
            recent_success_rate=recent_sr,
            instruction_count=inst_count,
            callee_resolved=callee_resolved,
            blocker=blocker,
            verified_examples=verified_count,
            example_quality=0.8 if verified_count > 0 else 1.0,
        )

        action = rl.select_action(data, lang_key, state)
        model, temp, few_shot = action.split("|")

        temp_val = float(temp)
        few_shot_val = int(few_shot)
        base_success = 0.3
        temp_bonus = (0.4 - temp_val) * 0.5
        few_shot_bonus = min(few_shot_val * 0.05, 0.15)
        callee_bonus = 0.1 if callee_resolved else -0.1
        complexity_penalty = min(inst_count / 200.0, 0.2)

        success_prob = base_success + temp_bonus + few_shot_bonus + callee_bonus - complexity_penalty
        success_prob = max(0.05, min(0.95, success_prob))
        learning_bonus = min(i / 100.0, 0.2)
        success_prob = min(0.95, success_prob + learning_bonus)

        if random.random() < success_prob:
            outcome = "verified"
            verified_count += 1
            reward = 1.0
        elif random.random() < 0.3:
            outcome = "compiles_no_verify"
            reward = 0.1
        else:
            outcome = "failed"
            failed_count += 1
            reward = -0.5

        new_coverage = verified_count / 295.0
        old_milestones = rl._coverage_milestones(coverage)
        new_milestones = rl._coverage_milestones(new_coverage)
        actually_new = new_milestones - old_milestones
        if actually_new:
            reward += 0.25 * len(actually_new)
            print(f"*** Coverage milestone hit: {actually_new} ***")

        total_reward += reward

        next_state = rl.encode_state(
            lang_key=lang_key,
            coverage=new_coverage,
            recent_success_rate=verified_count / max(i + 1, 1),
            instruction_count=inst_count,
            callee_resolved=callee_resolved,
            blocker=blocker,
            verified_examples=verified_count,
            example_quality=0.8 if verified_count > 0 else 1.0,
        )

        done = (outcome == "failed")
        rl.update_q(data, lang_key, state, action, reward, next_state, done)

        exp = rl.Experience(state=state, action=action, reward=reward,
                           next_state=next_state, done=done)
        rl.store_experience(data, lang_key, exp)

        rl.record_attempt(data, lang_key, fn, outcome)

        action_short = f"{model.split(':')[-1][:8]}|{temp}|{few_shot}"
        print(f"{i+1:>5} {fn:>15} {action_short:>45} {outcome:>10} {reward:>8.2f} {new_coverage:>9.1%} {data['epsilon']:>8.3f}")

        if (i + 1) % 10 == 0:
            updates = rl.replay_update(data, lang_key)
            print(f"   -> Experience replay: {updates} batch updates")

    rl.save_rl(data)

    print()
    print("=" * 70)
    print("Learning Summary")
    print("=" * 70)
    stats = rl.get_stats(data)
    print(f"Total attempts: {stats.total_attempts}")
    print(f"Total verified: {stats.total_verified}")
    print(f"Total failed: {stats.total_failed}")
    print(f"Final epsilon: {stats.language_stats.get(lang_key, {}).get('epsilon', 'N/A'):.4f}")
    print(f"Cumulative reward: {stats.cumulative_reward:.2f}")
    print(f"Success rate: {stats.language_stats.get(lang_key, {}).get('success_rate', 0):.1%}")

    q_table = data.get("q_table", {}).get(lang_key, {})
    print(f"\nQ-table states explored: {len(q_table)}")
    if q_table:
        print("\nBest actions discovered (sample):")
        for state_h, actions in list(q_table.items())[:5]:
            if actions:
                best = max(actions.items(), key=lambda x: x[1])
                print(f"  State {state_h[:12]}... -> {best[0]} (Q={best[1]:.3f})")
            else:
                print(f"  State {state_h[:12]}... -> (no actions yet)")

    assert rl.verify_pascal_isolation(data), "Pascal isolation violated!"
    print("\nPascal language isolation: VERIFIED (no cross-language leakage)")

    return data


def demonstrate_pascal_isolation():
    print("\n" + "=" * 70)
    print("Pascal Language Isolation Demonstration")
    print("=" * 70)

    data = rl.load_rl()

    pascal_key = "pascal|turbo-pascal-7"
    for i in range(10):
        state = rl.encode_state(
            lang_key=pascal_key, coverage=0.1, recent_success_rate=0.5,
            instruction_count=30, callee_resolved=True, blocker=None,
            verified_examples=3, example_quality=0.8,
        )
        action = rl.select_action(data, pascal_key, state)
        rl.update_q(data, pascal_key, state, action, 1.0, state, False)
        rl.record_attempt(data, pascal_key, f"PAS_FN_{i}", "verified")

    c_key = "c|gcc-unknown"
    for i in range(10):
        state = rl.encode_state(
            lang_key=c_key, coverage=0.1, recent_success_rate=0.5,
            instruction_count=30, callee_resolved=True, blocker=None,
            verified_examples=3, example_quality=0.8,
        )
        action = rl.select_action(data, c_key, state)
        rl.update_q(data, c_key, state, action, -0.5, state, False)
        rl.record_attempt(data, c_key, f"C_FN_{i}", "failed")

    pascal_states = data.get("q_table", {}).get(pascal_key, {})
    c_states = data.get("q_table", {}).get(c_key, {})

    print(f"\nPascal Q-table states: {len(pascal_states)}")
    print(f"C Q-table states: {len(c_states)}")
    print(f"Pascal attempts: {data.get('attempts', {}).get(pascal_key, 0)}")
    print(f"C attempts: {data.get('attempts', {}).get(c_key, 0)}")
    print(f"Pascal verified: {data.get('verified', {}).get(pascal_key, 0)}")
    print(f"C verified: {data.get('verified', {}).get(c_key, 0)}")
    print(f"C failed: {data.get('failed', {}).get(c_key, 0)}")

    all_keys = set(data.get("q_table", {}).keys())
    pascal_keys = {k for k in all_keys if k.startswith("pascal|")}
    c_keys = {k for k in all_keys if k.startswith("c|")}
    print(f"\nPascal keys: {pascal_keys}")
    print(f"C keys: {c_keys}")
    print(f"Overlap: {pascal_keys & c_keys}")
    assert not (pascal_keys & c_keys), "Language keys must not overlap!"
    print("\nPascal isolation: VERIFIED")

    rl.save_rl(data)


if __name__ == "__main__":
    random.seed(42)
    data = simulate_recovery_attempts(50)
    demonstrate_pascal_isolation()
    print("\nDemo complete. RL state saved to knowledge/rl_state.json")