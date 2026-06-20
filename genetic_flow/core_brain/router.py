import os
import re
import subprocess
import json
import sys
import sqlite3

# Ensure .matrix_ide/core is in path for kqml and rag
sys.path.append(os.path.expanduser("~/.matrix_ide/core"))
from kqml_protocol import KQMLMessage
from rag_pipeline import RAGController

class LocalAgentRouter:
    """[PERFORMATIVE: ROUTE] Native 32-bit llama-cli Wrapper with KQML/Vector Handoff."""

    def __init__(self, model_filename="danube3.gguf"):
        base_path = os.path.dirname(__file__)
        self.model_path = os.path.abspath(os.path.join(base_path, "..", "models", "h2o-danube3-500m-chat-Q4_K_M.gguf"))
        self.cli_path = os.path.abspath(os.path.join(base_path, "..", "models", "llama-cli-32bit"))
        self.rag = RAGController()

        if not os.path.exists(self.cli_path):
            # Fallback for mock/simulation if binary is missing during development
            self.mock_mode = True
        else:
            self.mock_mode = False

    def get_management_rules(self, level):
        conn = sqlite3.connect(os.path.expanduser("~/.matrix_ide/database/memory_foundation.db"))
        cur = conn.cursor()
        cur.execute("SELECT prompt_blueprint, management_logic FROM handoff_instructions WHERE level_target = ?", (level,))
        res = cur.fetchone()
        conn.close()
        return res if res else (None, None)

    def run_generation(self, task_intent, existing_code, temperature=0.7, extra_directive=""):
        # 1. Retrieve Precached Prompt Engineering & Local Management Rules
        blueprint, logic = self.get_management_rules("Neural")
        timeout_val = 1.0
        if logic and "timeout:" in logic:
            timeout_val = float(logic.split("timeout:")[1].split(",")[0])

        # 2. Retrieve context from Vector DB (KQML history)
        context = self.rag.search_context(task_intent, limit=2)
        context_str = "|".join(context)

        # 3. Apply Blueprint if available
        if blueprint:
            prompt = blueprint.format(intent=task_intent, context=context_str, code=existing_code)
        else:
            prompt = f"""<|prompt|>Goal: {task_intent}\nContext: {context_str}\nCode:\n{existing_code}\nOutput ONLY raw python code for 'def algorithm(n):'.<|endoftext|>\n<|answer|>"""

        try:
            if self.mock_mode:
                # Simulated high-speed response
                result_stdout = f"def algorithm(n):\n    return n * 2 # Optimized for {task_intent}"
            else:
                # Execute native 32-bit inference with DYNAMIC timeout from DB
                cmd = [
                    self.cli_path,
                    "-m", self.model_path,
                    "-p", prompt,
                    "-n", "64",
                    "--temp", str(temperature),
                    "--log-disable"
                ]
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_val)
                    result_stdout = result.stdout.strip()
                except subprocess.TimeoutExpired:
                    # Log BREAKDOWN to Vector DB
                    err_msg = KQMLMessage("error", "Router", "Neural", f"Timeout breakdown at {timeout_val}s", intent=task_intent)
                    self.rag.store_message(err_msg)
                    result_stdout = "def algorithm(n):\n    return n # Fallback (1s limit reached)"

            # Wrap result in KQML and store in Vector DB for handoff
            msg = KQMLMessage(
                performative="tell",
                sender="Neural-Router",
                receiver="Executive-Layer",
                content=result_stdout,
                intent=task_intent
            )
            self.rag.store_message(msg)

            return result_stdout
        except Exception as e:
            return f"def algorithm(n):\n    # Fallback due to error: {e}\n    return True"

    def clean_code(self, raw_stream):
        """Syntactic Cleaning Pass."""
        match = re.search(r'def algorithm\(.*?\):.*', raw_stream, re.DOTALL)
        if match:
            return match.group(0).strip()
        return raw_stream.strip()

def extract_clean_code(raw_stream):
    router = LocalAgentRouter()
    return router.clean_code(raw_stream)
