import threading
import time
from retransmission_protocol import GBN, SR
from congestion_control import RenoCongestionControl, VegasCongestionControl

WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024


class Sender:
    def __init__(
        self,
        server_socket,
        addr,
        congestion_control=RenoCongestionControl(),
        retransmission="SR",
    ):
        self.socket = server_socket
        self.addr = addr
        self.data = b""  # 待发送的数据

        self.congestion = congestion_control
        self.receive_ack = SR() if retransmission == "SR" else GBN

        self.timeout = TIMEOUT
        self.base = 0
        self.next_seq_num = 0
        self.lock = threading.Lock()
        self.timers = {}
        self.total_packets = 0
        print(f"总分组数：{self.total_packets}")

    def send_segment(self, seq_num):
        start_idx = seq_num * PACKET_SIZE
        end_idx = min((seq_num + 1) * PACKET_SIZE, len(self.data))
        packet_data = self.data[start_idx:end_idx]
        packet = seq_num.to_bytes(4, byteorder="big") + packet_data
        self.socket.sendto(packet, self.addr)
        self.send_times[seq_num] = time.time()  # 记录发送时间
        print(f"发送分组：{seq_num}")
        if seq_num not in self.timers:
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
        self.total_packets = (len(data) + PACKET_SIZE - 1) // PACKET_SIZE
        print(f"总分组数：{self.total_packets}")

        send_thread = threading.Thread(target=self.send_data)
        ack_thread = threading.Thread(target=self.receive_ack, args=(self,))
        send_thread.start()
        ack_thread.start()
        send_thread.join()
        ack_thread.join()
        print("文件发送完成")

    def send_data(self):
        while self.base < self.total_packets:
            with self.lock:
                while (
                    self.next_seq_num < self.base + self.congestion.get_window_size()
                    and self.next_seq_num < self.total_packets
                ):
                    self.send_segment(self.next_seq_num)
                    self.next_seq_num += 1
            time.sleep(0.1)
