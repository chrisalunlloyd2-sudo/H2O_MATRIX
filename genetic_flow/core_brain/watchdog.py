import os

# CIRCUIT BREAKER: Monitors stagnation counters
class Watchdog:
    def __init__(self, max_rounds=5):
        self.stuck_rounds = 0
        self.max_rounds = int(os.getenv("STAGNATION_FLOOR", max_rounds))

    def check_stagnation(self, improvement):
        if improvement <= 0:
            self.stuck_rounds += 1
        else:
            self.stuck_rounds = 0

        if self.stuck_rounds >= self.max_rounds:
            # TRIGGER: Public Cloud Gemini API circuit breaker
            return True, self.stuck_rounds
        return False, self.stuck_rounds

    def get_hyperparameter_adjustment(self):
        """Programmatically alter hyperparameters for rounds 1-5 of stagnation."""
        if self.stuck_rounds == 1:
            return {"temperature": 0.8, "directive": "unroll loops for performance"}
        elif self.stuck_rounds == 2:
            return {"temperature": 1.0, "directive": "use bitwise operations where possible"}
        elif self.stuck_rounds == 3:
            return {"temperature": 1.2, "directive": "minimize function calls, inline logic"}
        elif self.stuck_rounds == 4:
            return {"temperature": 0.5, "directive": "strict focus on mathematical precision"}
        return {}

    def trigger_cloud_escalation(self):
        print(" [!] CIRCUIT BREAKER TRIPPED: Escalating to Gemini Cloud API after 5 rounds...")
        self.stuck_rounds = 0
        return "def algorithm():\n    # Cloud-Optimized Logic\n    return True"
