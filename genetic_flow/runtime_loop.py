import hashlib
import os
import sys
import time
import subprocess
from dotenv import load_dotenv

# Add path for local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load configuration
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from genetic_flow.core_brain import router as r
from genetic_flow.core_brain import test_harness as qa
from genetic_flow.core_brain import watchdog as wb
from genetic_flow.core_brain import tui_layout as view
from genetic_flow.tracking_db import writer as w
from genetic_flow.symbolic_brain import extractor as sym
from rich.live import Live

def git_commit(message):
    try:
        # Surgical add to avoid noise
        subprocess.run(["git", "add", "genetic_flow/core_brain/target_feature.py"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        return True
    except: return False

def git_rollback():
    try:
        # Rollback ONLY the target file, never the infrastructure
        subprocess.run(["git", "checkout", "HEAD", "--", "genetic_flow/core_brain/target_feature.py"], check=True, capture_output=True)
        return True
    except: return False

def main_loop():
    goal = "Ensure algorithm(n) returns True or n for any integer n with max speed."
    current_passing_code = "def algorithm(n):\n    return False"
    current_passing_median = 999.0
    
    stagnation_monitor = wb.Watchdog(max_rounds=5)
    symbolic_bot = sym.SymbolicExtractor()
    target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "core_brain/target_feature.py"))
    
    with Live(view.generate_dashboard(0, 0.0, current_passing_code, 0, 5), refresh_per_second=4) as live:
        for generation in range(1, 1000000):
            # 1. Symbolic Extraction (Every 5 generations for testing)
            if generation % 5 == 0:
                symbolic_bot.analyze_patterns()

            # 2. Get Hyperparameter Adjustments
            h_params = stagnation_monitor.get_hyperparameter_adjustment()
            
            # 3. Generation & Extraction
            raw_output = r.run_generation(goal, current_passing_code, extra_directive=str(h_params))
            cleaned_code = r.extract_clean_code(raw_output)
            
            # 4. Physical Asset Code Stamp
            with open(target_path, "w") as f:
                f.write(cleaned_code)
            
            # 5. Evaluation
            fitness, ast_depth, median_lat = qa.evaluate()
            chash = hashlib.md5(cleaned_code.encode()).hexdigest()
            
            # 6. Selection Pressure & Atomic Sync
            improvement = current_passing_median - median_lat
            
            # Only accept improvement
            if median_lat > 0 and median_lat < current_passing_median:
                current_passing_code = cleaned_code
                current_passing_median = median_lat
                git_commit(f"Gen {generation}: Mutation {chash} | Latency: {median_lat:.6f}")
                w.store_mutation(chash, generation, fitness, cleaned_code, goal, ast_depth, stagnation_monitor.stuck_rounds, improvement)
                stagnation_monitor.check_stagnation(1.0)
            else:
                git_rollback()
                tripped, rounds = stagnation_monitor.check_stagnation(0)
                if tripped:
                    live.update(view.generate_dashboard(generation, fitness, "TRIGGERING CLOUD ESCALATION...", rounds, 5))
                    cloud_code = stagnation_monitor.trigger_cloud_escalation()
                    current_passing_code = cloud_code
                    with open(target_path, "w") as f: f.write(cloud_code)
                    git_commit(f"Gen {generation}: Cloud Escalation")
                    time.sleep(2)

            live.update(view.generate_dashboard(generation, fitness, current_passing_code, stagnation_monitor.stuck_rounds, 5))
            time.sleep(0.5)

if __name__ == "__main__":
    main_loop()
