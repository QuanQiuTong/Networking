import socket
import threading
import time
from util import upload, download

IP = "192.168.120.129"
# IP = "localhost"
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP, PORT)

    while True:
        op = input("请选择操作类型 (D)download/(U)upload、传输方式(GBN/SR)").strip().split()
        if len(op) == 2:
            operation, protocol = op
            break

    # 请求文件
    filename = input("请输入文件名：")

    handshake_message = (operation + " " + protocol).encode()

    # 重试机制
    retries = 0
    while retries < MAX_RETRIES:
        # 发送握手消息
        client_socket.sendto(handshake_message, server_address)
        print(f"发送握手消息到服务器：{operation} {protocol}")
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

    
    # 同样需要确保文件名发送成功
    retries = 0
    while retries < MAX_RETRIES:
        client_socket.sendto(filename.encode(), server_address)
        print(f"发送文件名到服务器：{filename}")
        # 等待服务器确认
        try:
            client_socket.settimeout(TIMEOUT)
            ack, _ = client_socket.recvfrom(1024)
            if ack.decode() == "FILENAME_ACK":
                print("服务器已确认文件名。")
                break
        except socket.timeout:
            print("等待服务器确认文件名超时，重试中...")
            retries += 1

    if retries == MAX_RETRIES:
        print("服务器未能确认文件名，连接失败。")
        client_socket.close()
        return

    if operation == "upload" or operation.upper() == "U":
        upload(filename, client_socket, server_address, protocol)
    elif operation == "download" or operation.upper() == "D":
        download(filename, client_socket, protocol)

    client_socket.close()

if __name__ == "__main__":
    main()