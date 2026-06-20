import sqlite3
import os
import subprocess

DB_PATH = os.path.expanduser("~/genetic_flow/tracking_db/memory.db")

def get_git_hash():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        return "no-git"

def store_mutation(chash, gen, score, code, task, ast_depth=0, stagnation=0, latency_delta=0.0):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    git_hash = get_git_hash()

    conn = sqlite3.connect(DB_PATH)
    # Step 1801: High-Speed PRAGMA optimizations (Pseudo-DuckDB performance)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000") # 64MB cache

    cursor = conn.cursor()
    # Updated Schema for Future Symbolic Bot ingestion
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS optimization_ledger (
            hash TEXT PRIMARY KEY,
            gen INTEGER,
            score REAL,
            code TEXT,
            task TEXT,
            git_hash TEXT,
            ast_depth INTEGER,
            stagnation_counter INTEGER,
            latency_delta REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        INSERT OR REPLACE INTO optimization_ledger
        (hash, gen, score, code, task, git_hash, ast_depth, stagnation_counter, latency_delta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (chash, gen, score, code, task, git_hash, ast_depth, stagnation, latency_delta))
    conn.commit()
    conn.close()
