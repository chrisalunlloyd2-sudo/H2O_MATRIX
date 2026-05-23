import asyncio
import json
import sqlite3
import os
import time

SOCKET_PATH = "/data/data/com.termux/files/usr/tmp/gemini_cli.sock"
DB_PATH = os.path.expanduser("~/.matrix_ide/database/memory_foundation.db")

async def process_and_store(payload):
    """The heavy lifting she does silently after your terminal is already free."""
    command = payload.get("command", "")
    exit_code = payload.get("exit_code", 0)
    
    # Simple semantic proxy (simulating embedding)
    embedding = [random.random() for _ in range(384)]
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO operational_memory (timestamp, embedding_json, payload, context_type)
        VALUES (?, ?, ?, ?)
    """, (time.time(), json.dumps(embedding), f"Cmd: {command} | Exit: {exit_code}", "cli_interaction"))
    conn.commit()
    conn.close()
    print(f" [Daemon] Logged: {command}")

async def handle_connection(reader, writer):
    """Instantly accepts data from your shell hook and releases it."""
    data = await reader.read(4096)
    writer.write(b"ACK")
    await writer.drain()
    writer.close()
    
    try:
        payload = json.loads(data.decode())
        asyncio.create_task(process_and_store(payload))
    except json.JSONDecodeError:
        pass

async def main():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
        
    server = await asyncio.start_unix_server(handle_connection, path=SOCKET_PATH)
    print(f"--- 🚀 GEMINI CLI DAEMON ACTIVE ON {SOCKET_PATH} ---")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    import random
    asyncio.run(main())
