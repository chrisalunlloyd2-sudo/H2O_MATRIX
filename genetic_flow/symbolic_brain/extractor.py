import sqlite3
import ast
import os

DB_PATH = os.path.expanduser("~/genetic_flow/tracking_db/memory.db")
RULES_PATH = os.path.expanduser("~/genetic_flow/symbolic_brain/rules.sql")

class SymbolicExtractor:
    """Extracts symbolic rules from successful mutations in the ledger."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def analyze_patterns(self):
        try:
            cursor = self.conn.cursor()
            # Query successful mutations
            cursor.execute("SELECT code, latency_delta FROM optimization_ledger WHERE score > 0 ORDER BY gen DESC LIMIT 20")
            rows = cursor.fetchall()
        except: return "Awaiting DB..."

        rules = []
        for code, delta in rows:
            try:
                tree = ast.parse(code)
                # Bitwise Optimization Detection
                has_bitwise = any(isinstance(node.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift))
                                  for node in ast.walk(tree) if isinstance(node, ast.BinOp))
                # Constant Folding / Unrolling Detection
                has_range_literal = any(isinstance(node.func, ast.Name) and node.func.id == 'range' and
                                        isinstance(node.args[0], ast.Constant) and node.args[0].value < 5
                                        for node in ast.walk(tree) if isinstance(node, ast.Call))

                if has_bitwise:
                    rules.append(f"-- Gen insight: Bitwise shift detected. Latency Delta: {delta:.8f}")
                if has_range_literal:
                    rules.append(f"-- Gen insight: Loop unrolling detected. Delta: {delta:.8f}")
                if "res =" in code and "return res" in code:
                    rules.append(f"-- Gen insight: Variable caching pattern detected.")
            except: continue

        # Deduplicate and persist
        unique_rules = list(set(rules))
        if unique_rules:
            # Step 1801: Merge with existing rules (preserve cluster biases)
            existing_rules = []
            if os.path.exists(RULES_PATH):
                with open(RULES_PATH, "r") as f:
                    existing_rules = [line.strip() for line in f.readlines()]

            combined = list(set(existing_rules + unique_rules))
            with open(RULES_PATH, "w") as f:
                f.write("\n".join(combined) + "\n")
            return f"Synchronized {len(combined)} symbolic axioms."
        return "Awaiting structural breakthroughs."

if __name__ == "__main__":
    extractor = SymbolicExtractor()
    print(extractor.analyze_patterns())
