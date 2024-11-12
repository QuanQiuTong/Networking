import socket
import threading
import time

# 定义GBN和SR协议的参数
WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024

class GBNReceiver:
    def __init__(self, client_socket):
        self.socket = client_socket
        self.expected_seq_num = 0
        self.file_data = b''

    def start(self):
        self.socket.settimeout(5)  # 设置超时时间为5秒
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 4)
                seq_num = int.from_bytes(packet[:4], byteorder='big')
                data = packet[4:]
                print(f"收到分组：{seq_num}")
                if seq_num == self.expected_seq_num:
                    self.file_data += data
                    ack_packet = seq_num.to_bytes(4, byteorder='big')
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK：{seq_num}")
                    self.expected_seq_num += 1
                else:
                    # 重复ACK上一个确认的序号
                    ack_packet = (self.expected_seq_num - 1).to_bytes(4, byteorder='big')
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送重复ACK：{self.expected_seq_num - 1}")
                if len(data) < PACKET_SIZE:
                    print("文件接收完成")
                    break
        except socket.timeout:
            print("接收超时")

class SRReceiver:
    def __init__(self, client_socket):
        self.socket = client_socket
        self.window_size = WINDOW_SIZE
        self.base = 0
        self.received_packets = {}
        self.file_data = b''

    def start(self):
        self.socket.settimeout(5)  # 设置超时时间为5秒
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 4)
                seq_num = int.from_bytes(packet[:4], byteorder='big')
                data = packet[4:]
                print(f"收到分组：{seq_num}")
                if self.base <= seq_num < self.base + self.window_size:
                    ack_packet = seq_num.to_bytes(4, byteorder='big')
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK：{seq_num}")
                    self.received_packets[seq_num] = data

                    while self.base in self.received_packets:
                        self.file_data += self.received_packets[self.base]
                        del self.received_packets[self.base]
                        self.base += 1
                else:
                    # 收到窗口外的分组，仍然发送ACK
                    ack_packet = seq_num.to_bytes(4, byteorder='big')
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK（窗口外）：{seq_num}")
                if len(data) < PACKET_SIZE:
                    print("文件接收完成")
                    break
        except socket.timeout:
            print("接收超时")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)

    # 选择传输方式
    protocol = input('请选择传输方式（GBN/SR）：').strip()
    client_socket.sendto(protocol.encode(), server_address)

    # 接收服务器发送的新端口号
    port_info, _ = client_socket.recvfrom(1024)
    new_port = int(port_info.decode())
    server_address = ('localhost', new_port)

    # 请求文件
    filename =  'test' # input('请输入要下载的文件名：')
    client_socket.sendto(filename.encode(), server_address)

    # 接收文件
    if protocol == 'GBN':
        receiver = GBNReceiver(client_socket)
        receiver.start()
        with open('download_' + filename, 'wb') as f:
            f.write(receiver.file_data)
    elif protocol == 'SR':
        receiver = SRReceiver(client_socket)
        receiver.start()
        with open('download_' + filename, 'wb') as f:
            f.write(receiver.file_data)
    client_socket.close()

if __name__ == '__main__':
    main()