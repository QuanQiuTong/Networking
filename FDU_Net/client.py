from socket import *
from datetime import datetime


def request(message) -> str:
    return (
        "POST / FDUnet/1.0\r\n"
        + "Date: "
        + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        + "\r\n"
        # + "Content-Length: "
        # + str(len(message))
        # + "\r\n"
        + "\r\n"
        + message
    )


serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while True:
    sentence = input("Input lowercase sentence:")
    clientSocket.send(request(sentence).encode())
    if sentence == "#quit":
        break
    modifiedSentence = clientSocket.recv(1024)
    print("From Server:\n" + modifiedSentence.decode())

clientSocket.close()

print("Connection closed")

input("Press Enter to exit...")
