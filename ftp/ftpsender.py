import socket
import threading
import time

# 定义GBN和SR协议的参数
WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024

class CongestionControl:
    def on_ack_received(self, ack_num):
        raise NotImplementedError

    def on_timeout(self, seq_num):
        raise NotImplementedError

    def get_window_size(self):
        raise NotImplementedError
    
class RenoCongestionControl(CongestionControl):
    def __init__(self):
        self.window_size = 1
        self.ssthresh = 64
        self.duplicate_acks = 0

    def on_ack_received(self, ack_num):
        if self.window_size < self.ssthresh:
            self.window_size += 1  # 慢启动阶段
        else:
            self.window_size += 1 / self.window_size  # 拥塞避免阶段
        self.duplicate_acks = 0

    def on_timeout(self, seq_num):
        self.ssthresh = max(self.window_size // 2, 1)
        self.window_size = 1
        self.duplicate_acks = 0

    def get_window_size(self):
        return self.window_size

def GBN(sender):
    while sender.base < sender.total_packets:
        ack_packet, _ = sender.socket.recvfrom(1024)
        ack_num = int.from_bytes(ack_packet, byteorder="big")
        print(f"收到ACK：{ack_num}")
        with sender.lock:
            if ack_num >= sender.base:
                for seq in range(sender.base, ack_num + 1):
                    if seq in sender.timers:
                        sender.timers[seq].cancel()
                        del sender.timers[seq]
                sender.base = ack_num + 1
                sender.congestion_control.on_ack_received(ack_num)
                # 继续发送下一个分组
                while (
                    sender.next_seq_num < sender.base + sender.congestion_control.get_window_size()
                    and sender.next_seq_num < sender.total_packets
                ):
                    sender.send_segment(sender.next_seq_num)
                    sender.next_seq_num += 1


# Closure
def SR():
    ack_received = {}

    def sr_receive_ack(sender):
        while sender.base < sender.total_packets:
            ack_packet, _ = sender.socket.recvfrom(1024)
            ack_num = int.from_bytes(ack_packet, byteorder="big")
            print(f"收到ACK：{ack_num}")
            with sender.lock:
                if ack_num in sender.timers:
                    sender.timers[ack_num].cancel()
                    del sender.timers[ack_num]
                    ack_received[ack_num] = True
                    sender.congestion_control.on_ack_received(ack_num)
                    while sender.base in ack_received:
                        del ack_received[sender.base]
                        sender.base += 1

    return sr_receive_ack
class Sender:
    def __init__(self, server_socket, addr, congestion_control = RenoCongestionControl(), retransmission = "SR"):
        self.receive_ack = SR() if retransmission == "SR" else GBN

        self.socket = server_socket
        self.addr = addr
        self.data = b"" # 待发送的数据

        self.congestion_control = congestion_control

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
        print(f"发送分组：{seq_num}")
        if seq_num not in self.timers:
            timer = threading.Timer(self.timeout, self.timeout_handler, args=(seq_num,))
            self.timers[seq_num] = timer
            timer.start()

    def timeout_handler(self, seq_num):
        with self.lock:
            print(f"超时重传分组：{seq_num}")
            self.congestion_control.on_timeout(seq_num)
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
                    self.next_seq_num < self.base + self.congestion_control.get_window_size()
                    and self.next_seq_num < self.total_packets
                ):
                    self.send_segment(self.next_seq_num)
                    self.next_seq_num += 1
            time.sleep(0.1)

