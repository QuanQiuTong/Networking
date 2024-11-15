import socket
import hashlib

WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024
log = print
# log = lambda *args, **kwargs: None


def save_file(filename, data, md5: str):
    if not data or data == b"":
        print("要下载的文件不存在 或 接收到的文件为空")
        return

    # 保存接收到的文件
    try:
        with open(filename, "wb") as f:
            f.write(data)
            print(f"成功写入文件，文件大小：{len(data)} 字节")
    except Exception as e:
        print("写入文件时发生错误：", e)

    # 校验MD5
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    local_md5 = md5_hash.hexdigest()

    if local_md5 == md5:
        print("文件校验正确")
    else:
        print("文件校验错误，接收到的MD5：", md5, "本地计算的MD5：", local_md5)
        # 根据需求处理校验失败的情况


def depacket(packet):
    return (
        int.from_bytes(packet[:4], byteorder="big"),
        packet[4] & 1,
        (packet[4] >> 1) & 1,
        packet[5:],
    )


class GBNReceiver:
    def __init__(self, client_socket, filename):
        self.socket = client_socket
        self.expected_seq = 0
        self.file_data = b""
        self.filename = filename
        self.received_md5 = ""

    def start(self):
        self.socket.settimeout(5)  # 设置超时时间为5秒
        try:
            while True:
                packet, addr = self.socket.recvfrom(PACKET_SIZE + 5)
                seq, fin, check, data = depacket(packet)
                log(f"expected_seq: {self.expected_seq}, seq: {seq}")
                log(f"收到分组：{seq}, FIN: {fin}, CHECK: {check}")
                if fin == 1 and seq == self.expected_seq:
                    log("接收到结束信号")
                    ack_packet = seq.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    log(f"发送ACK：{seq}")
                    break
                if check == 1 and seq == self.expected_seq:
                    log("接收到MD5校验码包")
                    self.received_md5 = data.decode()
                    ack_packet = seq.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    log(f"发送ACK（MD5）：{seq}")
                    self.expected_seq += 1
                elif seq == self.expected_seq:
                    self.file_data += data
                    log(f"接收分组{seq}, 长度{len(data)}, 总长度{len(self.file_data)}")
                    ack_packet = seq.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    log(f"发送ACK：{seq}")
                    self.expected_seq += 1
                else:
                    # 重复ACK上一个确认的序号
                    ack_packet = (self.expected_seq - 1).to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    log(f"发送重复ACK：{self.expected_seq - 1}")
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
                seq, fin, check, data = depacket(packet)
                log(f"收到分组：{seq}, FIN: {fin}, CHECK: {check}")
                if fin == 1 and seq == self.base:
                    log("接收到结束信号")
                    ack_packet = seq.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    log(f"发送ACK：{seq}")
                    break
                if self.base <= seq and seq < self.base + self.window_size:
                    ack_packet = seq.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    log(f"发送ACK：{seq}")
                    # 将 flags 和 data 一起存储
                    self.received_packets[seq] = (check, data)

                    while self.base in self.received_packets:
                        check, packet_data = self.received_packets[self.base]
                        if check == 1:
                            self.received_md5 = packet_data.decode()
                            log(f"接收到MD5校验码：{self.received_md5}")
                        else:
                            self.file_data += packet_data
                            log(
                                f"接收分组{seq}, 长度{len(data)}, 总长度{len(self.file_data)}"
                            )
                        del self.received_packets[self.base]
                        self.base += 1
                else:
                    # 收到窗口外的分组，仍然发送ACK
                    ack_packet = seq.to_bytes(4, byteorder="big")
                    self.socket.sendto(ack_packet, addr)
                    self.received_packets[seq] = (check, data)
                    log(f"发送ACK（窗口外）：{seq}")
        except socket.timeout:
            print("接收超时")

        save_file(self.filename, self.file_data, self.received_md5)
