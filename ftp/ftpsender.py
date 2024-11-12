import socket
import threading
import time

# 定义GBN和SR协议的参数
WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024


class GBNSender:
    def __init__(self, server_socket, addr, data):
        self.socket = server_socket
        self.addr = addr
        self.data = data
        self.window_size = WINDOW_SIZE
        self.timeout = TIMEOUT
        self.base = 0
        self.next_seq_num = 0
        self.lock = threading.Lock()
        self.timers = {}
        self.total_packets = (len(data) + PACKET_SIZE - 1) // PACKET_SIZE
        print(f"总分组数：{self.total_packets}")

    def send_segment(self, seq_num):
        start_idx = seq_num * PACKET_SIZE
        end_idx = min((seq_num + 1) * PACKET_SIZE, len(self.data))
        packet_data = self.data[start_idx:end_idx]
        packet = seq_num.to_bytes(4, byteorder="big") + packet_data
        self.socket.sendto(packet, self.addr)
        print(f"发送分组：{seq_num}")
        if seq_num not in self.timers:
            timer = threading.Timer(self.timeout, self.timeout_handler, args=(seq_num,))
            self.timers[seq_num] = timer
            timer.start()

    def timeout_handler(self, seq_num):
        print(f"超时重传分组：{seq_num}")
        self.send_segment(seq_num)

    def start(self):
        send_thread = threading.Thread(target=self.send_data)
        ack_thread = threading.Thread(target=self.receive_ack)
        send_thread.start()
        ack_thread.start()
        send_thread.join()
        ack_thread.join()

    def send_data(self):
        while self.base < self.total_packets:
            with self.lock:
                while (
                    self.next_seq_num < self.base + self.window_size
                    and self.next_seq_num < self.total_packets
                ):
                    self.send_segment(self.next_seq_num)
                    self.next_seq_num += 1
            time.sleep(0.1)

    def receive_ack(self):
        while self.base < self.total_packets:
            ack_packet, _ = self.socket.recvfrom(1024)
            ack_num = int.from_bytes(ack_packet, byteorder="big")
            print(f"收到ACK：{ack_num}")
            with self.lock:
                if ack_num >= self.base:
                    for seq in range(self.base, ack_num + 1):
                        if seq in self.timers:
                            self.timers[seq].cancel()
                            del self.timers[seq]
                    self.base = ack_num + 1
                    # 继续发送下一个分组
                    while (
                        self.next_seq_num < self.base + self.window_size
                        and self.next_seq_num < self.total_packets
                    ):
                        self.send_segment(self.next_seq_num)
                        self.next_seq_num += 1


class SRSender:
    def __init__(self, server_socket, addr, data):
        self.socket = server_socket
        self.addr = addr
        self.data = data
        self.window_size = WINDOW_SIZE
        self.timeout = TIMEOUT
        self.base = 0
        self.next_seq_num = 0
        self.lock = threading.Lock()
        self.timers = {}
        self.ack_received = {}
        self.total_packets = (len(data) + PACKET_SIZE - 1) // PACKET_SIZE
        print(f"总分组数：{self.total_packets}")

    def send_segment(self, seq_num):
        start_idx = seq_num * PACKET_SIZE
        end_idx = min((seq_num + 1) * PACKET_SIZE, len(self.data))
        packet_data = self.data[start_idx:end_idx]
        packet = seq_num.to_bytes(4, byteorder="big") + packet_data
        self.socket.sendto(packet, self.addr)
        print(f"发送分组：{seq_num}")
        if seq_num not in self.timers:
            timer = threading.Timer(self.timeout, self.timeout_handler, args=(seq_num,))
            self.timers[seq_num] = timer
            timer.start()

    def timeout_handler(self, seq_num):
        with self.lock:
            print(f"超时重传分组：{seq_num}")
            self.send_segment(seq_num)

    def start(self):
        send_thread = threading.Thread(target=self.send_data)
        ack_thread = threading.Thread(target=self.receive_ack)
        send_thread.start()
        ack_thread.start()
        send_thread.join()
        ack_thread.join()

    def send_data(self):
        while self.base < self.total_packets:
            with self.lock:
                while (
                    self.next_seq_num < self.base + self.window_size
                    and self.next_seq_num < self.total_packets
                ):
                    self.send_segment(self.next_seq_num)
                    self.next_seq_num += 1
            time.sleep(0.1)

    def receive_ack(self):
        while self.base < self.total_packets:
            ack_packet, _ = self.socket.recvfrom(1024)
            ack_num = int.from_bytes(ack_packet, byteorder="big")
            print(f"收到ACK：{ack_num}")
            with self.lock:
                if ack_num in self.timers:
                    self.timers[ack_num].cancel()
                    del self.timers[ack_num]
                    self.ack_received[ack_num] = True
                    while self.base in self.ack_received:
                        del self.ack_received[self.base]
                        self.base += 1
