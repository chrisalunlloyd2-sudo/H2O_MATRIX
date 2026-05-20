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
from rich.live import Live

def git_commit(message):
    try:
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        return True
    except:
        return False

def git_rollback():
    try:
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], check=True, capture_output=True)
        return True
    except:
        # If no previous commit, just discard changes
        subprocess.run(["git", "checkout", "--", "."], check=True, capture_output=True)
        return False

def main_loop():
    goal = "Ensure algorithm() yields explicitly True with maximum execution throughput."
    current_passing_code = "def algorithm():\n    return False"
    current_passing_median = 999.0 # High initial latency
    
    stagnation_monitor = wb.Watchdog(max_rounds=5)
    target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "core_brain/target_feature.py"))
    
    with Live(view.generate_dashboard(0, 0.0, current_passing_code, 0, 5), refresh_per_second=4) as live:
        for generation in range(1, 1000000):
            # 1. Get Hyperparameter Adjustments based on stagnation
            h_params = stagnation_monitor.get_hyperparameter_adjustment()
            
            # 2. Generation & Extraction
            raw_output = r.run_generation(goal, current_passing_code) # In real setup, pass h_params here
            cleaned_code = r.extract_clean_code(raw_output)
            
            # 3. Physical Asset Code Stamp (Atomic Write)
            with open(target_path, "w") as f:
                f.write(cleaned_code)
            
            # 4. Evaluation (Statistical Gating)
            fitness, ast_depth, median_lat = qa.evaluate()
            chash = hashlib.md5(cleaned_code.encode()).hexdigest()
            
            # 5. Selection Pressure & Atomic Sync
            improvement = current_passing_median - median_lat
            
            # Only accept if better than current baseline
            if median_lat > 0 and median_lat < current_passing_median:
                current_passing_code = cleaned_code
                current_passing_median = median_lat
                
                # Atomic Git Commit
                git_commit(f"Gen {generation}: Mutation {chash} | Latency: {median_lat:.6f}")
                
                # Persistence (Structured Logging)
                w.store_mutation(
                    chash=chash,
                    gen=generation,
                    score=fitness,
                    code=cleaned_code,
                    task=goal,
                    ast_depth=ast_depth,
                    stagnation=stagnation_monitor.stuck_rounds,
                    latency_delta=improvement
                )
                
                stagnation_monitor.check_stagnation(1.0) # Reset stagnation
            else:
                # Failure: Rollback Git State
                git_rollback()
                
                # Mark stagnation
                tripped, rounds = stagnation_monitor.check_stagnation(0)
                
                if tripped:
                    live.update(view.generate_dashboard(generation, fitness, "TRIGGERING CLOUD ESCALATION...", rounds, 5))
                    cloud_code = stagnation_monitor.trigger_cloud_escalation()
                    current_passing_code = cloud_code
                    with open(target_path, "w") as f:
                        f.write(cloud_code)
                    git_commit(f"Gen {generation}: Cloud Escalation")
                    time.sleep(2)

            # UI Update
            live.update(view.generate_dashboard(generation, fitness, current_passing_code, stagnation_monitor.stuck_rounds, 5))
            
            # Artificial delay to settle hardware
            time.sleep(0.5)

if __name__ == "__main__":
    main_loop()
