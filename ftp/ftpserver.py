import socket
import threading
from ftpsender2 import GBNSender, SRSender


def handle_client(addr, protocol, server_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定到随机可用端口
    client_socket.bind(("localhost", 0))
    # 将新的端口号告知客户端
    port_info = str(client_socket.getsockname()[1]).encode()
    server_socket.sendto(port_info, addr)

    # 在新的 socket 上接收文件名
    filename, _ = client_socket.recvfrom(1024)
    with open(filename.decode(), "rb") as f:
        data = f.read()
        print(f"成功读取文件，文件大小：{len(data)} 字节")
        if protocol == "GBN":
            sender = GBNSender(client_socket, addr, data)
            sender.start()
        elif protocol == "SR":
            sender = SRSender(client_socket, addr, data)
            sender.start()
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 12345))
    print("服务器已启动，等待客户端连接...")

    while True:
        protocol, addr = server_socket.recvfrom(1024)
        threading.Thread(
            target=handle_client, args=(addr, protocol.decode(), server_socket)
        ).start()


if __name__ == "__main__":
    main()
