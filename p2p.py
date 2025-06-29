# Import required libraries for networking, threading, system monitoring, and JSON handling
import socket
import threading
import time
import psutil
import json

# Define the port for peer-to-peer communication
PEER_PORT = 5000
# List of peer node IP addresses to communicate with
PEER_NODES = ["10.10.0.19"]

# Function to collect system resource usage (CPU and memory)
def get_system_status():
    # Get CPU usage percentage over a 1-second interval
    cpu_usage = psutil.cpu_percent(interval=1)
    # Get virtual memory statistics
    memory = psutil.virtual_memory()
    # Extract memory usage percentage
    memory_usage = memory.percent
    # Return a dictionary with CPU, memory usage, and system status
    return {"cpu": cpu_usage, "memory": memory_usage, "status": "online"}

# Function to broadcast system status to all peer nodes
def broadcast_status():
    while True:
        # Get current system status
        system_status = get_system_status()
        # Convert status to JSON and encode it to bytes
        status_message = json.dumps(system_status).encode('utf-8')
        # Iterate through each peer in the node list
        for peer in PEER_NODES:
            try:
                # Create a new socket for each peer connection
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # Connect to the peer on the specified port
                    s.connect((peer, PEER_PORT))
                    # Send the encoded status message
                    s.sendall(status_message)
            except ConnectionRefusedError:
                # Handle case where peer is offline
                print(f"Peer {peer} is offline.")
        # Wait 5 seconds before broadcasting again
        time.sleep(5)

# Function to listen for status updates from other peers
def listen_for_updates():
    # Create a server socket for listening
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the local host and specified port
        server_socket.bind(('', PEER_PORT))
        # Listen for incoming connections
        server_socket.listen()
        print("Listening for peer updates...")

        while True:
            # Accept incoming connections
            conn, addr = server_socket.accept()
            with conn:
                # Receive data (up to 1024 bytes)
                data = conn.recv(1024)
                if data:
                    # Decode and parse the JSON data
                    peer_status = json.loads(data.decode('utf-8'))
                    # Print the received status information
                    print(f"Received status from {addr[0]}: CPU={peer_status['cpu']}%, "
                          f"Memory={peer_status['memory']}%, Status={peer_status['status']}")

# Main execution block
if __name__ == "__main__":
    print("Starting P2P Network Monitoring System...")

    # Create a daemon thread for broadcasting status updates
    broadcast_thread = threading.Thread(target=broadcast_status)
    broadcast_thread.daemon = True
    broadcast_thread.start()

    # Create a daemon thread for listening to peer updates
    listen_thread = threading.Thread(target=listen_for_updates)
    listen_thread.daemon = True
    listen_thread.start()

    # Keep the main thread running to prevent program termination
    broadcast_thread.join()
    listen_thread.join()
