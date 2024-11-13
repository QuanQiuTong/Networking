import socket
import threading
from util import upload, download

IP = "192.168.3.17"
PORT = 25565

def handle_client(addr, operation, filename, protocol, congestion, server_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定到随机可用端口
    client_socket.bind((IP, 0))
    new_port = client_socket.getsockname()[1]
    print(f"为客户端 {addr} 分配新端口：{new_port}")
    
    # 将新的端口号告知客户端
    server_socket.sendto(str(new_port).encode(), addr)

    if operation == "download" or operation.upper() == "D":
        upload(filename, client_socket, addr, protocol, congestion)
    elif operation == "upload" or operation.upper() == "U":
        download(filename, client_socket, protocol, prefix="serverdown_")
    else:
        print("未知的操作类型。")
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))  # 尝试绑定到指定端口
    port = server_socket.getsockname()[1]
    print(f"服务器已启动，绑定端口号：{port}")

    while True:
        try:
            server_socket.settimeout(None)
            opc, addr = server_socket.recvfrom(1024)
            operation_protocol_congestion = opc.decode().strip()
            if not operation_protocol_congestion:
                continue
            parts = operation_protocol_congestion.split('|')
            if len(parts) >= 2:
                operation = parts[0]
                filename = parts[1]
                protocol = parts[2] if len(parts) > 2 else "GBN"
                congestion = parts[3] if len(parts) > 3 else "Reno"
            else:
                print("握手消息格式错误，忽略。")
                continue
            print(f"收到来自 {addr} 的请求：{operation} {filename} {protocol} {congestion}")
            # 启动新线程处理客户端请求
            threading.Thread(
                target=handle_client,
                args=(addr, operation, filename, protocol, congestion, server_socket),
            ).start()
        except Exception as e:
            print(f"处理客户端请求时发生错误：{e}")

if __name__ == "__main__":
    main()