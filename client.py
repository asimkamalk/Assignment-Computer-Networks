from os import environ as env
import socket


if __name__ == "__main__":
    port = int(env.get('PORT', 65432))
    host = env.get('HOST', '127.0.0.1')

    # In Docker Compose we pass the service name as hostname which Docker's
    # internal DNS resolves to appropriate container IP using host as-is will
    # return the passed name of the service so we will resolve the actual IP
    # of provided hostname
    host = socket.gethostbyname(host)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Successfully connected to socket server on tcp://{host}:{port}\n")

            while True:
                command = input("Enter a command (or 'exit' to quit): ")

                if command.lower() == 'exit':
                    break

                print("\nSending command to server...")

                s.send(command.encode('utf-8'))

                res = s.recv(2048).decode('utf-8')
                print(f"Server responded with")
                print("------------------------------------------------------------")
                print(res)
                print("------------------------------------------------------------\n")

    except Exception as e:
        print(f"Error: {e}")
