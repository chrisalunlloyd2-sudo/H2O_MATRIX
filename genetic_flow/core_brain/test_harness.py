import time
import sys
import os
import importlib
import random
import math

# Add current directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

class StatisticalEvaluator:
    """[PERFORMATIVE: EVALUATE] Evaluates microsecond trends via IQR variance algorithms (Pure Python)."""
    
    def __init__(self, run_count=50, warmups=10):
        self.run_count = run_count
        self.warmups = warmups

    def evaluate_performance(self):
        try:
            from . import target_feature
            importlib.reload(target_feature)
            
            latencies = []
            # Warmups
            for _ in range(self.warmups):
                target_feature.algorithm(random.randint(1, 100))
                
            # Profile Runs
            for _ in range(self.run_count):
                n = random.randint(1, 100)
                t0 = time.perf_counter()
                res = target_feature.algorithm(n)
                t1 = time.perf_counter()
                if res is not None:
                    latencies.append(t1 - t0)
            
            if not latencies: return 0, 0, 0
            
            # IQR Variance Filtering (Pure Python)
            latencies.sort()
            n = len(latencies)
            q1 = latencies[n // 4]
            q3 = latencies[(3 * n) // 4]
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            filtered = [x for x in latencies if lower_bound <= x <= upper_bound]
            if not filtered: filtered = latencies
            
            median_lat = filtered[len(filtered)//2]
            mean = sum(filtered) / len(filtered)
            variance = sum((x - mean) ** 2 for x in filtered) / len(filtered)
            
            fitness = 1.0 / (1.0 + median_lat * 1e6) 
            return fitness, median_lat, variance
        except Exception as e:
            # print(f" [!] Eval Error: {e}")
            return 0, 0, 0

def evaluate():
    evaluator = StatisticalEvaluator()
    return evaluator.evaluate_performance()
