import socket
import threading
import time
from util import upload, download

# IP = "192.168.120.129"
IP = "localhost"
PORT = 25565
TIMEOUT = 2  # 超时时间
MAX_RETRIES = 5  # 最大重试次数


def receive_port(client_socket):
    client_socket.settimeout(TIMEOUT)
    while True:
        try:
            port_info, _ = client_socket.recvfrom(1024)
            new_port = int(port_info.decode())
            return new_port
        except socket.timeout:
            return None


def main():
    while True:
        print("选择操作类型、重传协议和拥塞控制算法（参数使用空格分隔）:")
        print("<(D)download/(U)upload>  [*GBN/SR]  [*Reno/Vegas]:")
        op = input().strip().split()
        if len(op) >= 1:
            operation = op[0]
            protocol = op[1] if len(op) > 1 else "GBN"
            congestion = op[2] if len(op) > 2 else "Reno"
            break
    while True:
        filename = input("输入文件名 <filename>:")
        if filename:
            break

    # '|' 不是合法的文件名字符，可以用来分隔不同字段
    handshake_message = f"{operation}|{filename}|{protocol}|{congestion}".encode()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP, PORT)
    # 重试机制
    retries = 0
    while retries < MAX_RETRIES:
        # 发送握手消息
        client_socket.sendto(handshake_message, server_address)
        print(f"发送握手消息到服务器：{operation} {filename} {protocol} {congestion}")
        # 等待服务器响应
        new_port = receive_port(client_socket)
        if new_port:
            print(f"收到服务器新端口：{new_port}")
            break
        else:
            print("握手超时，重试中...")
            retries += 1

    if retries == MAX_RETRIES:
        print("无法与服务器建立连接，请稍后重试。")
        client_socket.close()
        return

    server_address = (IP, new_port)

    if operation == "upload" or operation.upper() == "U":
        upload(filename, client_socket, server_address, protocol, congestion)
    elif operation == "download" or operation.upper() == "D":
        download(filename, client_socket, protocol)

    client_socket.close()


if __name__ == "__main__":
    main()
