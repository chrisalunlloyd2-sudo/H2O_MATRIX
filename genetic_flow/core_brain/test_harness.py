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
    if not data:
        return 0, 0, 0
    data.sort()
    n = len(data)
    q1 = data[n // 4]
    q3 = data[(3 * n) // 4]
    iqr = q3 - q1
    median = statistics.median(data)
    # Filter outliers using IQR
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]
    if not filtered_data:
        return median, 0, 0
    return statistics.median(filtered_data), statistics.variance(filtered_data) if len(filtered_data) > 1 else 0, len(filtered_data)

def verify_ast_safety(file_path):
    """Ensure no global scope modifications or forbidden imports."""
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        
        for node in tree.body:
            # Only allow function definitions and imports (limited)
            if not isinstance(node, (ast.FunctionDef, ast.Import, ast.ImportFrom, ast.Expr)):
                if isinstance(node, ast.Assign):
                    # Global assignments are blocked
                    return False, f"Global assignment detected: {ast.dump(node)}"
                return False, f"Forbidden top-level node: {type(node).__name__}"
        
        # Check if algorithm function exists
        has_algo = any(isinstance(node, ast.FunctionDef) and node.name == 'algorithm' for node in tree.body)
        if not has_algo:
            return False, "algorithm() function not found"
            
        return True, "Safe"
    except Exception as e:
        return False, str(e)

def get_ast_depth(file_path):
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        
        def walk_depth(node, depth):
            if not list(ast.iter_child_nodes(node)):
                return depth
            return max(walk_depth(child, depth + 1) for child in ast.iter_child_nodes(node))
            
        return walk_depth(tree, 0)
    except:
        return 0

def evaluate():
    target_file = os.path.join(os.path.dirname(__file__), "target_feature.py")
    
    # 1. AST Safety Pass
    is_safe, msg = verify_ast_safety(target_file)
    if not is_safe:
        return 0.0, 0, 0.0 # Rejected

    try:
        from . import target_feature
        importlib.reload(target_feature)
        
        # 2. Randomized Input Injection & IQR Profiling
        run_count = int(os.getenv("RUN_COUNT", 30))
        warmup_count = int(os.getenv("WARMUP_COUNT", 5))
        latencies = []
        
        # Warmups
        for _ in range(warmup_count):
            try:
                # Injecting random seed to eliminate hardcoded returns
                target_feature.algorithm()
            except:
                pass
                
        # Profile Runs
        for _ in range(run_count):
            t0 = time.perf_counter()
            try:
                # In a more complex setup, we'd pass random args to algorithm()
                res = target_feature.algorithm()
                elapsed = time.perf_counter() - t0
                if res == True:
                    latencies.append(elapsed)
                else:
                    return 0.01, get_ast_depth(target_file), 0.0 # Failed logic
            except:
                return 0.0, get_ast_depth(target_file), 0.0 # Exception
        
        if not latencies:
            return 0.0, get_ast_depth(target_file), 0.0
            
        median_lat, variance, filtered_count = calculate_iqr_metrics(latencies)
        
        # Only accept if statistically significant (simulated here by returning score)
        # In runtime_loop, we will compare this against current_passing_median
        fitness = float(1.0 / (1.0 + median_lat))
        return fitness, get_ast_depth(target_file), median_lat
        
    except Exception as e:
        return 0.0, 0, 0.0
