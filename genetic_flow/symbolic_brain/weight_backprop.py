import sqlite3
import os
import math

MEMORY_DB = os.path.expanduser("~/genetic_flow/tracking_db/memory.db")

class WeightBackprop:
    """[PERFORMATIVE: UPDATE] Calculates code fitness improvements and updates rule weights."""

    def __init__(self, db_path=MEMORY_DB):
        self.db_path = db_path

    def update_rule_weights(self, rule_id, fitness_improvement):
        """Increments or decrements target rule index weights based on harness outcomes."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Learning rate (simulated)
            lr = 0.1

            if fitness_improvement > 0:
                # Success: Increment weight and success count
                # Logarithmic adjustment: W_new = W_old + LR * log(1 + improvement)
                adjustment = lr * math.log(1 + fitness_improvement * 1000)
                cursor.execute("""
                    UPDATE production_rules
                    SET current_rule_weight = current_rule_weight + ?,
                        success_count = success_count + 1
                    WHERE rule_id = ?
                """, (adjustment, rule_id))
            else:
                # Failure: Decrement weight and failure count
                cursor.execute("""
                    UPDATE production_rules
                    SET current_rule_weight = current_rule_weight - 0.05,
                        failure_count = failure_count + 1
                    WHERE rule_id = ?
                """, (rule_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Backprop Error: {e}")
            return False

if __name__ == "__main__":
    backprop = WeightBackprop()
    backprop.update_rule_weights(1, 0.005)
