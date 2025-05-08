PortHunter
Description: This tool scans a target network for open ports and tries to determine the services running on those ports. It can be used to discover potential attack surfaces on a network.

 (Python):

python
Copy
Edit
import socket

def scan_ports(target):
    open_ports = []
    for port in range(1, 1024):  # Scan ports 1-1024
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

if __name__ == "__main__":
    target = input("Enter the target IP address to scan: ")
    open_ports = scan_ports(target)
    print(f"Open ports on {target}: {open_ports}")
