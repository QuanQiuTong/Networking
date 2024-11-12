import socket
from ftpreceiver import GBNReceiver, SRReceiver
from ftpsender import Sender


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", 12345)

    # 选择操作类型
    operation = input("请选择操作类型（download/upload）：").strip()
    client_socket.sendto(operation.encode(), server_address)

    # 选择传输方式
    protocol = input("请选择传输方式（GBN/SR）：").strip()
    client_socket.sendto(protocol.encode(), server_address)

    # 接收服务器发送的新端口号
    port_info, _ = client_socket.recvfrom(1024)
    new_port = int(port_info.decode())
    server_address = ("localhost", new_port)

    # 请求文件
    filename = "test"  # input('请输入要下载的文件名：')
    client_socket.sendto(filename.encode(), server_address)

    if operation == "upload":
        sender = Sender(client_socket, server_address, retransmission=protocol)
        with open(filename, "rb") as f:
            data = f.read()
            print(f"成功读取文件，文件大小：{len(data)} 字节")
            sender.start(data)
    elif operation == "download":
        receiver = (
            protocol == "GBN"
            and GBNReceiver(client_socket)
            or SRReceiver(client_socket)
        )
        receiver.start()
        with open("download_" + filename, "wb") as f:
            f.write(receiver.file_data)

    client_socket.close()


if __name__ == "__main__":
    main()
