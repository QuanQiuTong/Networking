from socket import *
from threading import Thread
from datetime import datetime


def response(state, sentence="") -> str:
    return (
        "1.0 "
        + state
        + "\r\n"
        + "Date: "
        + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        + "\r\n\r\n"
        + sentence
    )


def handle_client(connectionSocket, addr):
    print(f"Connection from {addr}")
    while True:
        sentence = connectionSocket.recv(1024).decode()
        print(f"Received from {addr}:\n{sentence}")
        message = sentence.split("\r\n\r\n")[1]

        if sentence.startswith("POST / FDUnet/1.0") and message:
            if message == "#quit":
                break
            message = message.upper()
            connectionSocket.send(response("200 OK", message).encode())

        else:
            connectionSocket.send(response("501 Not Implemented").encode())
    connectionSocket.close()
    print(f"Connection with {addr} closed")


def main():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(5)
    print("The server is ready to receive")

    while True:
        connectionSocket, addr = serverSocket.accept()
        client_thread = Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()


if __name__ == "__main__":
    main()
