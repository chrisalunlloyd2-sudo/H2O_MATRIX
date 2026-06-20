import sqlite3
import os
import time

DB_PATH = os.path.expanduser("~/.matrix_ide/database/ledger.db")

def initialize_cluster_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS cluster_nodes (id INTEGER PRIMARY KEY, status TEXT, last_heartbeat INTEGER)")
    # Seed local node
    conn.execute("INSERT OR IGNORE INTO cluster_nodes (id, status, last_heartbeat) VALUES (0, 'ONLINE', ?)", (int(time.time()),))
    conn.commit()
    conn.close()

def update_heartbeat(node_id=0):
    """Updates the heartbeat for a specific cluster node."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE cluster_nodes SET last_heartbeat = ? WHERE id = ?", (int(time.time()), node_id))
        conn.commit()
        conn.close()
    except: pass

def get_cluster_topology():
    """Returns a string representation of the cluster topology for the TUI."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, status, last_heartbeat FROM cluster_nodes")
        nodes = cursor.fetchall()
        conn.close()

        topo_str = "CLUSTER TOPOLOGY:\n"
        now = int(time.time())
        for nid, status, heartbeat in nodes:
            latency = now - heartbeat
            state = "ACTIVE" if latency < 10 else "STALE"
            topo_str += f" [Node-{nid}] {status} | Latency: {latency}s | {state}\n"
        return topo_str
    except Exception as e:
        return f"Topology Error: {e}"

if __name__ == "__main__":
    initialize_cluster_table()
    print(get_cluster_topology())
