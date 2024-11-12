import socket

WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024


class GBNReceiver:
    def __init__(self, client_socket):
        self.socket = client_socket
        self.expected_seq_num = 0
        self.file_data = b""

    def start(self):
        self.socket.settimeout(5)  # 设置超时时间为5秒
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 4)
                seq_num = int.from_bytes(packet[:4], byteorder="big")
                data = packet[4:]
                print(f"收到分组：{seq_num}")
                if seq_num == self.expected_seq_num:
                    self.file_data += data
                    ack_packet = seq_num.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK：{seq_num}")
                    self.expected_seq_num += 1
                else:
                    # 重复ACK上一个确认的序号
                    ack_packet = (self.expected_seq_num - 1).to_bytes(
                        4, byteorder="big"
                    )
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
        self.file_data = b""

    def start(self):
        self.socket.settimeout(5)  # 设置超时时间为5秒
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 4)
                seq_num = int.from_bytes(packet[:4], byteorder="big")
                data = packet[4:]
                print(f"收到分组：{seq_num}")
                if self.base <= seq_num < self.base + self.window_size:
                    ack_packet = seq_num.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK：{seq_num}")
                    self.received_packets[seq_num] = data

                    while self.base in self.received_packets:
                        self.file_data += self.received_packets[self.base]
                        del self.received_packets[self.base]
                        self.base += 1
                else:
                    # 收到窗口外的分组，仍然发送ACK
                    ack_packet = seq_num.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK（窗口外）：{seq_num}")
                if len(data) < PACKET_SIZE:
                    print("文件接收完成")
                    break
        except socket.timeout:
            print("接收超时")
