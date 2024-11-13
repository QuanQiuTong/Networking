import socket
import hashlib

WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024


def save_file(filename, data, md5):
    # 保存接收到的文件
    with open(filename, "wb") as f:
        f.write(data)
        print(f"成功写入文件，文件大小：{len(data)} 字节")

    # 校验MD5
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    local_md5 = md5_hash.hexdigest()

    if local_md5 == md5:
        print("文件校验正确")
    else:
        print("文件校验错误，接收到的MD5：", md5, "本地计算的MD5：", local_md5)
        # 根据需求处理校验失败的情况


class GBNReceiver:
    def __init__(self, client_socket, filename):
        self.socket = client_socket
        self.expected_seq_num = 0
        self.file_data = b""
        self.filename = filename
        self.received_md5 = ""

    def start(self):
        self.socket.settimeout(5)  # 设置超时时间为5秒
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 5)
                seq_num = int.from_bytes(packet[:4], byteorder="big")
                flags = packet[4]
                fin_flag = flags & 1
                check_flag = (flags >> 1) & 1
                data = packet[5:]
                print(f"收到分组：{seq_num}, FIN: {fin_flag}, CHECK: {check_flag}")
                if fin_flag == 1:
                    print("接收到结束信号")
                    break
                elif check_flag == 1 and seq_num == self.expected_seq_num:
                    print("接收到MD5校验码包")
                    self.received_md5 = data.decode()
                    ack_packet = seq_num.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK（MD5）：{seq_num}")
                    self.expected_seq_num += 1
                elif seq_num == self.expected_seq_num:
                    self.file_data += data
                    print(
                        f"接收分组：{seq_num}, 数据长度：{len(data)}, 文件总长度：{len(self.file_data)}"
                    )
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
        except socket.timeout:
            print("接收超时")

        save_file(self.filename, self.file_data, self.received_md5)


class SRReceiver:
    def __init__(self, client_socket, filename):
        self.socket = client_socket
        self.window_size = WINDOW_SIZE
        self.base = 0
        self.received_packets = {}
        self.file_data = b""
        self.filename = filename
        self.received_md5 = ""

    def start(self):
        self.socket.settimeout(5)
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 5)
                seq_num = int.from_bytes(packet[:4], byteorder="big")
                flags = packet[4]
                fin_flag = flags & 1
                check_flag = (flags >> 1) & 1
                data = packet[5:]
                print(f"收到分组：{seq_num}, FIN: {fin_flag}, CHECK: {check_flag}")
                if fin_flag == 1:
                    print("接收到结束信号")
                    break
                elif self.base <= seq_num < self.base + self.window_size:
                    ack_packet = seq_num.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK：{seq_num}")
                    # 将 flags 和 data 一起存储
                    self.received_packets[seq_num] = (flags, data)

                    while self.base in self.received_packets:
                        packet_flags, packet_data = self.received_packets[self.base]
                        check_flag = (packet_flags >> 1) & 1
                        if check_flag == 1:
                            self.received_md5 = packet_data.decode()
                            print(f"接收到MD5校验码：{self.received_md5}")
                        else:
                            self.file_data += packet_data
                            print(
                                f"接收分组：{self.base}, 数据长度：{len(packet_data)}, 文件总长度：{len(self.file_data)}"
                            )
                        del self.received_packets[self.base]
                        self.base += 1
                else:
                    # 收到窗口外的分组，仍然发送ACK
                    ack_packet = seq_num.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    print(f"发送ACK（窗口外）：{seq_num}")
        except socket.timeout:
            print("接收超时")

        save_file(self.filename, self.file_data, self.received_md5)
