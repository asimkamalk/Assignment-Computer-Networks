import socket
import subprocess
from os import environ as env
import threading


def get_addr(client_address):
    return f"{client_address[0]}:{client_address[1]}"


def run_command(command):
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"


def handle_client(client_socket, client_address):
    print(f"Started new thread for handling connection with {get_addr(client_address)}\n")

    with client_socket:
        while True:
            data = client_socket.recv(2048).decode('utf-8')

            # The client will send a message with an empty payload when it
            # wants to close the connection
            if not data or not data.strip():
                break

            print(f"Received command from {get_addr(client_address)}: {data}")
            result = run_command(data)
            client_socket.send(result.encode('utf-8'))
            print("Responded client with results\n")

    print(f"Connection with {get_addr(client_address)} closed\n")


if __name__ == "__main__":
    port = int(env.get('PORT', 65432))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen()

        print(f"Socket connection open to local network on port {port}")

        while True:
            client_socket, client_address = s.accept()
            print(f"\nReceived new socket connection from {get_addr(client_address)}")

            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

