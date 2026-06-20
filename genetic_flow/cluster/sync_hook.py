import sqlite3
import os
import json

LEDGER_DB = os.path.expanduser("~/.matrix_ide/database/ledger.db")
MEMORY_DB = os.path.expanduser("~/genetic_flow/tracking_db/memory.db")

def sync_bayesian_weights():
    """Bridge ledger.db quantum_parameters into the genetic flow loop."""
    print("--- 🚀 CLUSTER SYNC: BRIDGE INITIATED ---")

    if not os.path.exists(LEDGER_DB):
        print(f" [!] Error: Main ledger not found at {LEDGER_DB}")
        return

    # 1. Extract weights from Main Ledger
    try:
        conn_ledger = sqlite3.connect(LEDGER_DB)
        cursor = conn_ledger.cursor()
        cursor.execute("SELECT value FROM quantum_parameters WHERE key='weights'")
        row = cursor.fetchone()
        conn_ledger.close()

        if row:
            weights = json.loads(row[0])
            print(f" [*] Synchronized Bayesian Weights: {weights}")

            # 2. Inject into Genetic Flow (rules.sql or .env)
            # We'll append them as symbolic rules for now
            rules_path = os.path.expanduser("~/genetic_flow/symbolic_brain/rules.sql")
            with open(rules_path, "a") as f:
                f.write(f"\n-- Cluster Weight Bias: {row[0]}\n")
            print(" [Step 3001] BRIDGE: Weights injected into Symbolic Brain.")
    except Exception as e:
        print(f" [!] Sync Error: {e}")

def export_optimization_stats():
    """Export genetic progress back to the main IDE ledger."""
    if not os.path.exists(MEMORY_DB): return

    try:
        conn_mem = sqlite3.connect(MEMORY_DB)
        cursor_mem = conn_mem.cursor()
        cursor_mem.execute("SELECT hash, score, code FROM optimization_ledger ORDER BY gen DESC LIMIT 1")
        best = cursor_mem.fetchone()
        conn_mem.close()

        if best:
            chash, score, code = best
            conn_ledger = sqlite3.connect(LEDGER_DB)
            cursor_ledger = conn_ledger.cursor()
            # Push into code_variants or a cluster status table
            cursor_ledger.execute("INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                                 ("best_genetic_variant", f"{chash}:{score}"))
            conn_ledger.commit()
            conn_ledger.close()
            print(f" [Step 3010] BRIDGE: Best variant {chash[:8]} exported to Main Ledger.")
    except Exception as e:
        print(f" [!] Export Error: {e}")

if __name__ == "__main__":
    sync_bayesian_weights()
    export_optimization_stats()
    print("--- SYNC COMPLETE: Matrix Cluster Nodes Converged ---")
