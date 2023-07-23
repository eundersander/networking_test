import socket
import time

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    while True:
        client_socket.sendall("marco".encode())
        print("Sent: marco")

        data = client_socket.recv(1024).decode()
        if data == "polo":
            print("Received:", data)

        time.sleep(1)

    client_socket.close()

if __name__ == '__main__':
    run_client()