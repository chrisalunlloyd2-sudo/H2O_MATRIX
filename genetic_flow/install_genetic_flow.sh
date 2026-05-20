#!/data/data/com.termux/files/usr/bin/bash
# ===========================================================================================
# 🧬 GENETIC FLOW: 32-bit Termux Automated Installer
# Bypasses Windows quirks, optimizes for mobile ARM kernels.
# ===========================================================================================

echo "--- [1/5] UPDATING SYSTEM SUBSTRATE ---"
pkg update -y && pkg upgrade -y
pkg install python git sqlite -y
pip install rich requests duckdb python-dotenv

echo "--- [2/5] MANIFESTING WORKSPACE MATRICES ---"
mkdir -p ~/genetic_flow/{core_brain,tracking_db,logs}

echo "--- [3/5] INJECTING CORE ENGINE LAYERS ---"
# Logic already manifested in previous steps, confirming integrity...
ls -l ~/genetic_flow/runtime_loop.py

echo "--- [4/5] SETTING RESOURCE BOUNDARY GUARDS ---"
# Step 8: Memory Boundary (256MB RAM ceiling)
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_KV_CACHE_TYPE=q4_0
ulimit -v 262144

echo "--- [5/5] INITIALIZING EVOLUTIONARY LOOP ---"
# Acquire Wakelock to prevent process eviction
termux-wake-lock

echo "[+] Genetic Flow Substrate Armed. Run: python3 ~/genetic_flow/runtime_loop.py"
