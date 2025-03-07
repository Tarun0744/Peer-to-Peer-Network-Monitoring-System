import socket
import threading
import time
import psutil
import json

PEER_PORT = 5000
PEER_NODES=["10.10.0.19"]

def get_system_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    return {"cpu": cpu_usage, "memory": memory_usage, "status": "online"}

def broadcast_status():
    while True:
        system_status = get_system_status()
        status_message = json.dumps(system_status).encode('utf-8')
        for peer in PEER_NODES:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((peer, PEER_PORT))
                    s.sendall(status_message)
            except ConnectionRefusedError:
                print(f"Peer {peer} is offline.")
        time.sleep(5)

def listen_for_updates():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', PEER_PORT))
        server_socket.listen()
        print("Listening for peer updates...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    peer_status = json.loads(data.decode('utf-8'))
                    print(f"Received status from {addr[0]}: CPU={peer_status['cpu']}%, "
                          f"Memory={peer_status['memory']}%, Status={peer_status['status']}")

if __name__ == "__main__":
    print("Starting P2P Network Monitoring System...")

    broadcast_thread = threading.Thread(target=broadcast_status)
    broadcast_thread.daemon = True
    broadcast_thread.start()

    listen_thread = threading.Thread(target=listen_for_updates)
    listen_thread.daemon = True
    listen_thread.start()

    broadcast_thread.join()
    listen_thread.join()
