import socket
import json
import sys

SOCKET_PATH = "/data/data/com.termux/files/usr/tmp/gemini_cli.sock"

def send_to_daemon(command, exit_code):
    payload = json.dumps({
        "command": command,
        "exit_code": exit_code
    })
    
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(SOCKET_PATH)
        sock.sendall(payload.encode())
        sock.recv(1024) 
        sock.close()
    except Exception:
        pass

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        send_to_daemon(sys.argv[1], int(sys.argv[2]))
