import socket
import threading
from ftpsender import Sender
from util import upload, download

IP = "172.17.40.155"
PORT = 25565

def handle_client(addr, operation, protocol, server_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定到随机可用端口
    client_socket.bind((IP, 0))
    # 将新的端口号告知客户端
    port_info = str(client_socket.getsockname()[1]).encode()
    server_socket.sendto(port_info, addr)

    # 在新的 socket 上接收文件名
    filename, _ = client_socket.recvfrom(1024)
    if operation == "download":
        upload(filename.decode(), client_socket, addr, protocol)

    elif operation == "upload":
        download(filename.decode(), client_socket, protocol, prefix="serverdown_")

    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))  # 绑定到随机可用端口
    port = server_socket.getsockname()[1]  # 获取绑定的端口号
    print(f"服务器已启动，绑定端口号：{port}")

    while True:
        operation, addr = server_socket.recvfrom(1024)
        protocol, addr = server_socket.recvfrom(1024)
        threading.Thread(
            target=handle_client,
            args=(addr, operation.decode(), protocol.decode(), server_socket),
        ).start()


if __name__ == "__main__":
    main()
