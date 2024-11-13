import threading
import time
import hashlib
from retransmission_protocol import GBN, SR
from congestion_control import RenoCongestionControl

WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024


class Sender:
    def __init__(
        self,
        socket,
        addr,
        congestion_control=RenoCongestionControl(),
        retransmission="SR",
    ):
        self.socket = socket
        self.addr = addr
        self.data = b""

        self.congestion = congestion_control
        self.receive_ack = SR() if retransmission == "SR" else GBN

        self.send_times = {}  # 用于记录发送时间
        self.timeout = TIMEOUT
        self.base = 0
        self.next_seq_num = 0
        self.lock = threading.Lock()
        self.timers = {}
        self.total_packets = 0
        self.stop_event = threading.Event()

        self.socket.settimeout(3)  # 设置超时时间为3秒

    def send_segment(self, seq_num, fin=False, data=b""):
        chk = seq_num == self.total_packets - 1
        start_idx = seq_num * PACKET_SIZE
        end_idx = min((seq_num + 1) * PACKET_SIZE, len(self.data))
        if not chk:
            packet_data = self.data[start_idx:end_idx]
        else:
            packet_data = self.md5_data

        flags = 0
        
        if fin:
            flags |= 1  # FIN标志位
        if chk:
            flags |= 2  # CHECK标志位
        flags_byte = flags.to_bytes(1, byteorder="big")

        packet = seq_num.to_bytes(4, byteorder="big") + flags_byte + packet_data
        self.socket.sendto(packet, self.addr)
        self.send_times[seq_num] = time.time()  # 记录发送时间
        print(f"发送分组：{seq_num}, FIN: {fin}, CHECK: {chk}, len: {len(packet)}, start: {start_idx}, end: {end_idx}")
        if seq_num not in self.timers and not fin:
            timer = threading.Timer(self.timeout, self.timeout_handler, args=(seq_num,))
            self.timers[seq_num] = timer
            timer.start()

    def timeout_handler(self, seq_num):
        with self.lock:
            print(f"超时重传分组：{seq_num}")
            self.congestion.on_timeout(seq_num)
            self.send_segment(seq_num)

    def start(self, data):
        self.data = data

        md5_hash = hashlib.md5()
        md5_hash.update(self.data)
        self.md5_data = md5_hash.hexdigest().encode()

        # 将 total_packets 加 1，包括 MD5 校验码包
        self.total_packets = (len(data) + PACKET_SIZE - 1) // PACKET_SIZE
        self.total_packets += 1
        print(f"总分组数：{self.total_packets}")

        send_thread = threading.Thread(target=self.send_data)
        ack_thread = threading.Thread(target=self.receive_ack, args=(self,))
        send_thread.start()
        ack_thread.start()
        send_thread.join()
        ack_thread.join()
        print("文件发送完成")

        # 发送结束信号
        self.send_segment(self.total_packets, fin=True)
        self.stop()

    def send_data(self):
        # 计算 MD5 校验码

        while self.base < self.total_packets and not self.stop_event.is_set():
            with self.lock:
                while (
                    self.next_seq_num < self.base + self.congestion.get_window_size()
                    and self.next_seq_num < self.total_packets
                ):
                    # 发送数据包
                    self.send_segment(self.next_seq_num)
                    self.next_seq_num += 1
            time.sleep(0.1)

    def stop(self):
        self.stop_event.set()
        self.socket.close()