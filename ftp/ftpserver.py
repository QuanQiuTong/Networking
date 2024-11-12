import socket
import threading
from ftpsender import Sender
from ftpreceiver import GBNReceiver, SRReceiver


def handle_client(addr, operation, protocol, server_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定到随机可用端口
    client_socket.bind(("localhost", 0))
    # 将新的端口号告知客户端
    port_info = str(client_socket.getsockname()[1]).encode()
    server_socket.sendto(port_info, addr)

    # 在新的 socket 上接收文件名
    filename, _ = client_socket.recvfrom(1024)
    if operation == "download":
        sender = Sender(client_socket, addr, retransmission=protocol)
        with open(filename.decode(), "rb") as f:
            data = f.read()
            print(f"成功读取文件，文件大小：{len(data)} 字节")
            sender.start(data)
    elif operation == "upload":
        receiver = (
            protocol == "GBN"
            and GBNReceiver(client_socket)
            or SRReceiver(client_socket)
        )
        receiver.start()
        with open("serverdown_" + filename.decode(), "wb") as f:
            f.write(receiver.file_data)

    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 12345))
    print("服务器已启动，等待客户端连接...")

    while True:
        operation, addr = server_socket.recvfrom(1024)
        protocol, addr = server_socket.recvfrom(1024)
        threading.Thread(
            target=handle_client,
            args=(addr, operation.decode(), protocol.decode(), server_socket),
        ).start()


if __name__ == "__main__":
    main()
