import socket, threading, json

HOST = "0.0.0.0"
PORT = 5555

clients = {}        # pid -> socket
players_data = {}   # pid -> last known state

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

def handle_client(conn, addr):
    pid = str(addr)
    clients[pid] = conn
    players_data[pid] = {"x":0,"y":0,"name":"???","color":[255,0,0]}
    print(f"[JOIN] Player connected: {pid}")
    buffer = ""

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data.decode()
            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                if not msg.strip():
                    continue
                try:
                    pdata = json.loads(msg)
                    players_data[pid] = pdata
                except:
                    continue

            # Broadcast all players to everyone
            all_data = json.dumps(players_data) + "\n"
            for c in clients.values():
                try:
                    c.sendall(all_data.encode())
                except:
                    pass
    except Exception as e:
        print(f"[ERROR] Player {pid} error: {e}")
    finally:
        print(f"[DISCONNECT] Player disconnected: {pid} (name: {players_data.get(pid, {}).get('name','???')})")
        del clients[pid]
        del players_data[pid]
        conn.close()

print(f"Server running on {HOST}:{PORT}")
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
