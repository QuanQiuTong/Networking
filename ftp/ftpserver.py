import socket
import threading
import time
from util import upload, download

IP = "localhost"
PORT = 25565
TIMEOUT = 5  # 超时时间

def handle_client(addr, operation, protocol, server_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定到随机可用端口
    client_socket.bind((IP, 0))
    new_port = client_socket.getsockname()[1]
    print(f"为客户端 {addr} 分配新端口：{new_port}")
    
    # 将新的端口号告知客户端
    server_socket.sendto(str(new_port).encode(), addr)

    # 在新的 socket 上接收文件名
    client_socket.settimeout(TIMEOUT)
    try:
        filename, client_addr = client_socket.recvfrom(1024)
        filename = filename.decode()
        print(f"收到客户端请求的文件名：{filename}")
        # 发送确认消息
        client_socket.sendto("FILENAME_ACK".encode(), client_addr)
    except socket.timeout:
        print(f"在新端口 {new_port} 上等待文件名超时，关闭连接。")
        client_socket.close()
        return

    if operation == "download" or operation.upper() == "D":
        upload(filename, client_socket, client_addr, protocol)
    elif operation == "upload" or operation.upper() == "U":
        download(filename, client_socket, protocol, prefix="serverdown_")
    else:
        print("未知的操作类型。")
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))  # 绑定到指定端口
    print(f"服务器已启动，绑定端口号：{PORT}")

    while True:
        try:
            server_socket.settimeout(None)
            op, addr = server_socket.recvfrom(1024)
            operation_protocol = op.decode().strip()
            if not operation_protocol:
                continue
            operation, protocol = operation_protocol.split()
            print(f"收到来自 {addr} 的请求：{operation} {protocol}")
            # 启动新线程处理客户端请求
            threading.Thread(
                target=handle_client,
                args=(addr, operation, protocol, server_socket),
            ).start()
        except Exception as e:
            print(f"处理客户端请求时发生错误：{e}")

if __name__ == "__main__":
    main()