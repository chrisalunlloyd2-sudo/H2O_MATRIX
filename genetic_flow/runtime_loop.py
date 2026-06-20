import os
import sys
import time
import hashlib
from dotenv import load_dotenv

# Add local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from genetic_flow.core_brain import router as r
from genetic_flow.core_brain import test_harness as qa
from genetic_flow.symbolic_brain import engine as sym
from genetic_flow.core_brain import tui_layout as view
from genetic_flow.tracking_db import writer as w
from genetic_flow.core_brain.binary_engine.decompiler import BinaryDecompilationEngine
from rich.live import Live

import argparse

def main_loop(max_gen=1000):
    goal = "Optimize algorithm(n) for max throughput."
    current_code = "def algorithm(n):\n    return n > 0"
    current_median = 999.0

    # Initialize Engines
    context_engine = sym.SymbolicContextEngine()
    rule_matcher = sym.ProductionRuleMatcher()
    backpropagator = sym.WeightBackpropagator()
    injector = sym.MutationInjector()
    router = r.LocalAgentRouter()
    decompiler = BinaryDecompilationEngine()

    # Track binary entropy
    current_entropy = decompiler.decompile_and_score(current_code)
    target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "core_brain/target_feature.py"))

    with Live(view.generate_dashboard(0, 0, current_code, 0, 5), refresh_per_second=4) as live:
        for gen in range(1, max_gen + 1):
            # 1. TOKENIZE
            signature = context_engine.get_structural_signature(current_code)
            c_hash = context_engine.generate_context_hash(signature)

            # 2. MATCH
            rule_id, directive, weight = rule_matcher.match_rule(c_hash) or (1, "global", 1.0)

            # 3. GENERATE
            raw_gen = router.run_generation(goal, current_code, extra_directive=directive)
            mutated_code = r.extract_clean_code(raw_gen)

            # 4. INJECT
            final_code = injector.apply_mutation(mutated_code, directive)
            with open(target_path, "w") as f:
                f.write(final_code)

            # 5. EVALUATE + BINARY MATH
            start_eval = time.time()
            fitness, median_lat, variance = qa.evaluate()
            eval_duration = time.time() - start_eval

            new_entropy = decompiler.decompile_and_score(final_code)

            # 6. SELECTION PRESSURE (Latency + Entropy)
            success = (median_lat < current_median) or (new_entropy < current_entropy)

            # 7. BACKPROPAGATE
            backpropagator.backprop(rule_id, success)

            if success:
                current_code = final_code
                current_median = median_lat
                current_entropy = new_entropy

                context_engine.update_relational_matrix(current_code)
                w.store_mutation(c_hash, gen, fitness, current_code, goal)
            else:
                with open(target_path, "w") as f:
                    f.write(current_code)

            # --- RESOURCE CONSTRAINTS (25% CPU CAP + 5S DELAY) ---
            cooldown = eval_duration * 3
            time.sleep(cooldown + 5.0)

            # --- SCIENTIFIC LOGGING ---
            with open("SCIENTIFIC_LOG.md", "a") as log:
                log.write(f"\n### Generation {gen} (Step 9 Equivalent)\n")
                log.write(f"- **Observation**: Latency={median_lat:.2f}ms, Entropy={new_entropy:.4f}\n")
                log.write(f"- **Hypothesis**: Mutation with directive '{directive}' improves fitness.\n")
                log.write(f"- **Result**: {'SUCCESS' if success else 'FAILURE'} (Score: {fitness})\n")

            live.update(view.generate_dashboard(gen, fitness, current_code, 0, 5))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-gen", type=int, default=1000)
    args = parser.parse_args()
    main_loop(max_gen=args.max_gen)
