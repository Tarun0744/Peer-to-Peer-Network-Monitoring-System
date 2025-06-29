# Peer to Peer Network Monitoring System
## Overview
This project implements a Peer-to-Peer (P2P) Network Monitoring System using Python. It enables nodes in a network to broadcast their system resource usage (CPU and memory) to other peers and receive updates from them. The system uses socket programming for communication and multithreading to handle broadcasting and listening concurrently.

## Features
- Monitors CPU and memory usage of the local system.
- Broadcasts system status to specified peer nodes every 5 seconds.
- Listens for status updates from other peer nodes.
- Displays received peer status, including CPU usage, memory usage, and online status.
- Handles offline peers gracefully with error logging.

## Prerequisites
To run this project, you need the following:
- Python 3.6 or higher
- Required Python library:
  - `psutil`: For system resource monitoring

Install the required library using pip:
```bash
pip install psutil
```

## Project Structure
- `p2p.py`: The main script for the P2P network monitoring system.
- `README.md`: This file, providing an overview and instructions for the project.

## Usage
1. **Configure Peer Nodes**:
   - Edit the `PEER_NODES` list in `p2p_monitor.py` to include the IP addresses of the peer nodes you want to communicate with.
   - Example: `PEER_NODES = ["192.168.1.100", "192.168.1.101"]`
   - Ensure all nodes are running the same script and listening on the same port (`PEER_PORT = 5000` by default).

2. **Run the Script**:
   ```bash
   python p2p.py
   ```
   - The script starts two threads:
     - One broadcasts the local system's CPU and memory usage to all peers every 5 seconds.
     - Another listens for status updates from other peers and prints them to the console.

3. **Expected Output**:
   - On startup: `Starting P2P Network Monitoring System...` and `Listening for peer updates...`
   - For each offline peer: `Peer <IP> is offline.`
   - For received updates: `Received status from <IP>: CPU=<value>%, Memory=<value>%, Status=online`

4. **Stopping the Program**:
   - Press `Ctrl+C` to terminate the program. The daemon threads will exit gracefully.

## Notes
- Ensure that all peer nodes are accessible and not blocked by firewalls.
- The `PEER_PORT` (default: 5000) must be open on all nodes.
- The system assumes a reliable network; consider adding more robust error handling for production use.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built using Python’s `socket`, `threading`, and `psutil` libraries.
- Inspired by simple P2P networking applications.
