import time
import socket

PACKET_SIZE = 1024



def GBN(sender):
    while sender.base < sender.total_packets and not sender.stop_event.is_set():
        try:
            ack_packet, _ = sender.socket.recvfrom(1024)
            ack_num = int.from_bytes(ack_packet, byteorder="big")
            rtt = time.perf_counter() - sender.send_times[ack_num]
            # print(f"收到ACK：{ack_num}, RTT: {rtt}")
        except socket.timeout:
            # 超时处理，重传未确认的分组
            print("ACK 接收超时，重传未确认的分组")
            for seq in range(sender.base, sender.next_seq_num):
                sender.timeout_handler(seq)
        except Exception as e:
            print(f"接收ACK时发生错误：{e}")
            continue
        with sender.lock:
            if ack_num >= sender.base:
                for seq in range(sender.base, ack_num + 1):
                    if seq in sender.timers:
                        sender.timers[seq].cancel()
                        del sender.timers[seq]
                sender.base = ack_num + 1
                sender.congestion.on_ack_received(ack_num, rtt)
                while (
                    sender.next_seq_num
                    < sender.base + sender.congestion.get_window_size()
                    and sender.next_seq_num < sender.total_packets
                ):
                    sender.send_segment(sender.next_seq_num)
                    sender.next_seq_num += 1


def SR():
    ack_received = {}

    def sr_receive_ack(sender):
        while sender.base < sender.total_packets and not sender.stop_event.is_set():
            try:
                ack_packet, _ = sender.socket.recvfrom(1024)
                ack_num = int.from_bytes(ack_packet, byteorder="big")
                rtt = time.perf_counter() - sender.send_times[ack_num]
                # print(f"收到ACK：{ack_num}, RTT: {rtt}")
            except socket.timeout:
                # 超时处理，重传未确认的分组
                print("ACK 接收超时，重传未确认的分组")
                for seq in range(sender.base, sender.next_seq_num):
                    if seq not in ack_received: # and seq in sender.timers:
                        sender.timeout_handler(seq)
            except Exception as e:
                print(f"接收ACK时发生错误：{e}")
                continue
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
