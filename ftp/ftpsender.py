import threading
import time
import hashlib
from retransmission_protocol import GBN, SR
from congestion_control import Reno, Vegas

WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024

log = print
# log = lambda *args, **kwargs: None

class Sender:
    def __init__(self, socket, addr, retransmission, congestion_control=Reno()):
        self.socket = socket
        self.addr = addr
        self.data = b""

        self.congestion = Reno() if congestion_control == "Reno" else Vegas()
        self.receive_ack = GBN if retransmission == "GBN" else SR()

        self.send_times = {}  # 用于记录发送时间
        self.timeout = TIMEOUT
        self.base = 0
        self.next_seq_num = 0
        self.lock = threading.Lock()
        self.timers = {}
        self.total_packets = 0
        self.stop_event = threading.Event()

        self.socket.settimeout(6)  # 设置超时时间为6秒

    def send_segment(self, seq: int, fin=False):
        chk = seq == self.total_packets - 1
        start_idx = seq * PACKET_SIZE
        end_idx = min((seq + 1) * PACKET_SIZE, len(self.data))
        if not chk:
            packet_data = self.data[start_idx:end_idx]
        else:
            packet_data = self.md5_data

        flags = (chk << 1) | fin

        packet = seq.to_bytes(4, "big") + flags.to_bytes(1, "big") + packet_data
        self.socket.sendto(packet, self.addr)
        self.send_times[seq] = time.perf_counter()  # 记录发送时间
        log(f"发送分组：{seq}, FIN: {fin}, CHECK: {chk}, len: {len(packet)}, start: {start_idx}, end: {end_idx}")
        if seq not in self.timers and not fin:
            timer = threading.Timer(self.timeout, self.timeout_handler, args=(seq,))
            self.timers[seq] = timer
            timer.start()

    def timeout_handler(self, seq):
        with self.lock:
            log(f"超时重传分组：{seq}")
            self.congestion.on_timeout(seq)
            self.send_segment(seq)

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

        start_time = time.perf_counter()
        send_thread.start()
        ack_thread.start()
        send_thread.join()
        ack_thread.join()
        end_time = time.perf_counter()
        print("文件发送完成")

        throughput = len(data) / (end_time - start_time)
        print(f"有效吞吐量：{throughput:.2f} Byte/s")
        utilization = len(data) / (self.total_packets * PACKET_SIZE)
        print(f"流量利用率：{utilization:.2f}")

        # 发送结束信号
        self.send_segment(self.total_packets, fin=True)
        self.stop()

    def send_data(self):
        while self.base < self.total_packets and not self.stop_event.is_set():
            with self.lock:
                while (
                    self.next_seq_num < self.base + self.congestion.get_window_size()
                    and self.next_seq_num < self.total_packets
                ):
                    # 发送数据包
                    self.send_segment(self.next_seq_num)
                    self.next_seq_num += 1
            # time.sleep(0.1)

    def stop(self):
        self.stop_event.set()
        self.socket.close()
