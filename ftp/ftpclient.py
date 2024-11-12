import socket
from util import upload, download

IP = "47.254.120.45"
PORT = 44382


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP, PORT)

    # 选择操作类型
    operation = input("请选择操作类型（download/upload）：").strip()
    client_socket.sendto(operation.encode(), server_address)

    # 选择传输方式
    protocol = input("请选择传输方式（GBN/SR）：").strip()
    client_socket.sendto(protocol.encode(), server_address)

    # 接收服务器发送的新端口号
    port_info, _ = client_socket.recvfrom(1024)
    new_port = int(port_info.decode())
    server_address = (IP, new_port)

    # 请求文件
    filename = "test"  # input('请输入要下载的文件名：')
    client_socket.sendto(filename.encode(), server_address)

    if operation == "upload":
        upload(filename, client_socket, server_address, protocol)
    elif operation == "download":
        download(filename, client_socket, protocol)

    client_socket.close()


if __name__ == "__main__":
    main()
