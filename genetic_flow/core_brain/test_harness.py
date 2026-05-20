import time
import sys
import os
import importlib
import ast
import random
import statistics

# Add current directory to path to ensure target_feature is found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def calculate_iqr_metrics(data):
    if not data: return 0, 0, 0
    data.sort()
    n = len(data)
    q1 = data[n // 4]
    q3 = data[(3 * n) // 4]
    iqr = q3 - q1
    median = statistics.median(data)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]
    if not filtered_data: return median, 0, 0
    return statistics.median(filtered_data), statistics.variance(filtered_data) if len(filtered_data) > 1 else 0, len(filtered_data)

def verify_ast_safety(file_path):
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.Import, ast.ImportFrom, ast.Expr)):
                return False, "Safety Violation"
        return True, "Safe"
    except: return False, "Parse Error"

def get_ast_depth(file_path):
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        def walk_depth(node, depth):
            if not list(ast.iter_child_nodes(node)): return depth
            return max(walk_depth(child, depth + 1) for child in ast.iter_child_nodes(node))
        return walk_depth(tree, 0)
    except: return 0

def evaluate():
    target_file = os.path.join(os.path.dirname(__file__), "target_feature.py")
    safe, _ = verify_ast_safety(target_file)
    if not safe: return 0.0, 0, 0.0

    try:
        from . import target_feature
        importlib.reload(target_feature)
        
        run_count = int(os.getenv("RUN_COUNT", 30))
        warmup_count = int(os.getenv("WARMUP_COUNT", 5))
        latencies = []
        
        test_inputs = [random.randint(1, 100) for _ in range(run_count + warmup_count)]
        
        for i in range(warmup_count):
            try: target_feature.algorithm(test_inputs[i])
            except: pass
                
        for i in range(run_count):
            val = test_inputs[warmup_count + i]
            t0 = time.perf_counter()
            try:
                res = target_feature.algorithm(val)
                elapsed = time.perf_counter() - t0
                if res == True or res == val:
                    latencies.append(elapsed)
                else: return 0.01, get_ast_depth(target_file), 0.0
            except: return 0.0, get_ast_depth(target_file), 0.0
        
        if not latencies: return 0.0, get_ast_depth(target_file), 0.0
        
        median_lat, _, _ = calculate_iqr_metrics(latencies)
        median_lat = max(median_lat, 1e-9) * (1.0 + (random.random() - 0.5) * 0.002)
        
        fitness = float(1.0 / (1.0 + median_lat))
        return fitness, get_ast_depth(target_file), median_lat
        
    except Exception: return 0.0, 0, 0.0
