import time

def GBN(sender):
    while sender.base < sender.total_packets:
        ack_packet, _ = sender.socket.recvfrom(1024)
        ack_num = int.from_bytes(ack_packet, byteorder="big")
        rtt = time.time() - sender.send_times[ack_num]  # 计算RTT
        print(f"收到ACK：{ack_num}, RTT: {rtt}")
        with sender.lock:
            if ack_num >= sender.base:
                for seq in range(sender.base, ack_num + 1):
                    if seq in sender.timers:
                        sender.timers[seq].cancel()
                        del sender.timers[seq]
                sender.base = ack_num + 1
                sender.congestion.on_ack_received(ack_num, rtt)
                # 继续发送下一个分组
                while (
                    sender.next_seq_num < sender.base + sender.congestion.get_window_size()
                    and sender.next_seq_num < sender.total_packets
                ):
                    sender.send_segment(sender.next_seq_num)
                    sender.next_seq_num += 1

# Closure, return a SR receiver function
def SR():
    ack_received = {}

    def sr_receive_ack(sender):
        while sender.base < sender.total_packets:
            ack_packet, _ = sender.socket.recvfrom(1024)
            ack_num = int.from_bytes(ack_packet, byteorder="big")
            rtt = time.time() - sender.send_times[ack_num]  # 计算RTT
            print(f"收到ACK：{ack_num}, RTT: {rtt}")
            with sender.lock:
                if ack_num in sender.timers:
                    sender.timers[ack_num].cancel()
                    del sender.timers[ack_num]
                    ack_received[ack_num] = True
                    sender.congestion.on_ack_received(ack_num, rtt)
                    while sender.base in ack_received:
                        del ack_received[sender.base]
                        sender.base += 1

    return sr_receive_ack