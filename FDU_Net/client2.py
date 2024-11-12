from socket import *


serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while True:
    sentence = input("Input request:")
    clientSocket.send(sentence.encode())
    if sentence == "#quit":
        break
    modifiedSentence = clientSocket.recv(1024)
    print("From Server:", modifiedSentence.decode())

clientSocket.close()
