import ast
import subprocess
import os
import sys

TARGET_FILE = os.path.expanduser("~/genetic_flow/core_brain/target_feature.py")

class CodeSprite:
    """Autonomous Dependency Sprite: Scans for imports and manifests environment."""
    
    def __init__(self):
        self.installed_packages = self._get_installed_packages()

    def _get_installed_packages(self):
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
            return result.stdout.lower()
        except:
            return ""

    def scan_and_fix(self):
        print("--- 🧚 CODE SPRITE: SCANNING FOR DEPENDENCIES ---")
        if not os.path.exists(TARGET_FILE): return
        
        try:
            with open(TARGET_FILE, "r") as f:
                tree = ast.parse(f.read())
            
            required_modules = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        required_modules.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        required_modules.append(node.module.split('.')[0])

            for module in set(required_modules):
                # Basic check: skip standard library (simplistic for demo)
                if module in sys.builtin_module_names or module in ['os', 'sys', 'time', 'math', 're', 'json', 'hashlib', 'sqlite3', 'subprocess']:
                    continue
                
                if module not in self.installed_packages:
                    print(f" [!] Missing Dependency Detected: {module}")
                    print(f" [Step 4001] MANIFESTING: pip install {module}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", module], check=True)
                    print(f" [Step 4010] REPAIRED: {module} is now available.")
                else:
                    print(f" [*] Dependency Validated: {module}")

        except Exception as e:
            print(f" [!] Sprite Error: {e}")

if __name__ == "__main__":
    sprite = CodeSprite()
    sprite.scan_and_fix()
    print("--- SPRITE PASS COMPLETE: Environment Synchronized ---")
