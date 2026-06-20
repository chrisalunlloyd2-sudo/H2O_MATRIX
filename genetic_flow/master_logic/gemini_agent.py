#!/usr/bin/env python3
import asyncio
import subprocess
import json
import sys
import os
import hashlib
import asyncpg
from openai import AsyncOpenAI
from genetic_flow.core_brain.binary_engine.decompiler import BinaryDecompilationEngine

# Logic-Airgapped Configuration
client = AsyncOpenAI()
DB_DSN = "postgres://user:pass@localhost:5432/gemini_rag"

async def get_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return response.data[0].embedding

async def fetch_memory_context(goal: str) -> tuple[str, str]:
    async with asyncpg.create_pool(dsn=DB_DSN) as pool:
        async with pool.acquire() as conn:
            constraints = await conn.fetch("SELECT content FROM core_constraints")
            goal_vector = await get_embedding(goal)
            history = await conn.fetch("""
                SELECT content, metadata
                FROM operational_memory
                ORDER BY embedding <=> $1
                LIMIT 3
            """, str(goal_vector))

    sys_constraints = "Immutable Rules:\n" + "".join([f"- {r['content']}\n" for r in constraints])
    op_history = "Past Context/Fixes:\n" + "".join([f"- {r['content']} (Meta: {r['metadata']})\n" for r in history])
    return sys_constraints, op_history

async def run_cmd(cmd: str) -> tuple[int, str]:
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return process.returncode, (process.stdout + process.stderr).strip()

async def fix_step(step_data: dict, error_output: str, sys_constraints: str, decompiler: BinaryDecompilationEngine, max_retries: int = 3):
    messages = [
        {"role": "system", "content": (
            "You are an autonomous RAM-Fenced agent. Previous command failed. "
            "Output ONLY valid JSON: {\"command\": \"new fix command\"}\n\n"
            + sys_constraints
        )},
        {"role": "user", "content": f"Action: {step_data['action_cmd']}\nError: {error_output}"}
    ]

    for attempt in range(max_retries):
        response = await client.chat.completions.create(
            model="gpt-4o", messages=messages, response_format={"type": "json_object"}, temperature=0.1
        )
        fix_cmd = json.loads(response.choices[0].message.content).get("command", "")

        # Binary Entropy Optimization Gate
        pre_entropy = decompiler.decompile_and_score(step_data['action_cmd'])
        await run_cmd(fix_cmd)
        post_entropy = decompiler.decompile_and_score(fix_cmd)

        v_code, v_out = await run_cmd(step_data['verify_cmd'])
        if v_code == 0 and post_entropy <= pre_entropy:
            return True

        messages.append({"role": "user", "content": f"Failed (Entropy delta: {post_entropy-pre_entropy}). Fix again."})
    return False

async def main(goal: str):
    sys_constraints, op_history = await fetch_memory_context(goal)
    decompiler = BinaryDecompilationEngine()

    # 1. GENERATE PLAN
    messages = [{"role": "system", "content": "You are a master architect. Output JSON plan."}, {"role": "user", "content": f"Goal: {goal}\n\n{op_history}"}]
    response = await client.chat.completions.create(model="gpt-4o", messages=messages, response_format={"type": "json_object"})
    plan = json.loads(response.choices[0].message.content).get("plan", [])

    # 2. EXECUTE & VERIFY
    for step in plan:
        await run_cmd(step['action_cmd'])
        v_code, v_out = await run_cmd(step['verify_cmd'])
        if v_code != 0:
            await fix_step(step, v_out, sys_constraints, decompiler)

if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:])))
