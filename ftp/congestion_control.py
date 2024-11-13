# 定义GBN和SR协议的参数
WINDOW_SIZE = 4
TIMEOUT = 2
PACKET_SIZE = 1024


class CongestionControl:
    def on_ack_received(self, ack_num, rtt):
        raise NotImplementedError

    def on_timeout(self, seq_num):
        raise NotImplementedError

    def get_window_size(self):
        raise NotImplementedError


class Reno(CongestionControl):
    def __init__(self):
        self.window_size = 1  # 拥塞窗口（cwnd）
        self.ssthresh = 64    # 慢启动阈值
        self.duplicate_acks = 0
        self.last_ack_num = -1

    def on_ack_received(self, ack_num, rtt=None):
        if ack_num == self.last_ack_num:
            # 收到重复的 ACK
            self.duplicate_acks += 1
            if self.duplicate_acks == 3:
                # 快速重传
                self.ssthresh = max(self.window_size // 2, 2)
                self.window_size = self.ssthresh
                print("触发快速重传，调整 ssthresh 和窗口大小")
                self.duplicate_acks = 0
        else:
            # 收到新的 ACK
            self.duplicate_acks = 0
            if self.window_size < self.ssthresh:
                # 慢启动阶段，指数增长
                self.window_size += 1
                print(f"慢启动阶段，窗口大小增至：{self.window_size}")
            else:
                # 拥塞避免阶段，线性增长
                self.window_size += 1 / self.window_size
                print(f"拥塞避免阶段，窗口大小增至：{self.window_size:.2f}")
        self.last_ack_num = ack_num

    def on_timeout(self, seq_num):
        # 超时处理，进入慢启动
        self.ssthresh = max(self.window_size // 2, 2)
        self.window_size = 1
        self.duplicate_acks = 0
        self.last_ack_num = -1
        print(f"发生超时，调整 ssthresh={self.ssthresh}，窗口大小重置为 1")

    def get_window_size(self):
        return max(1, int(self.window_size))


class Vegas(CongestionControl):
    def __init__(self):
        self.window_size = 1  # 拥塞窗口（cwnd）
        self.ssthresh = 64    # 慢启动阈值
        self.base_rtt = None
        self.alpha = 1
        self.beta = 3
        self.duplicate_acks = 0
        self.last_ack_num = -1
        self.ewma_alpha = 0.125  # 平滑系数

    def on_ack_received(self, ack_num, rtt):
        MIN_RTT = 0.001  # 最小 RTT 值，单位秒

        if self.base_rtt is None:
            self.base_rtt = rtt  # 初始化 base_rtt
            print(f"初始化 base_rtt：{self.base_rtt}")
            return

        if ack_num == self.last_ack_num:
            # 收到重复的 ACK
            self.duplicate_acks += 1
            if self.duplicate_acks == 3:
                # 快速重传
                self.ssthresh = max(self.window_size // 2, 2)
                self.window_size = self.ssthresh
                print("触发快速重传（Vegas），调整 ssthresh 和窗口大小")
                self.duplicate_acks = 0
        else:
            # 收到新的 ACK
            self.duplicate_acks = 0
            if rtt > 0:
                smoothed_rtt = (self.ewma_alpha * rtt + (1 - self.ewma_alpha) * self.base_rtt)
                self.base_rtt = min(self.base_rtt, smoothed_rtt)
            else:
                print("警告：RTT 为零或负值，使用最小 RTT")
                smoothed_rtt = self.base_rtt

            expected_rate = self.window_size / max(self.base_rtt, MIN_RTT)
            actual_rate = self.window_size / max(smoothed_rtt, MIN_RTT)
            diff = expected_rate - actual_rate

            if self.window_size < self.ssthresh:
                # 慢启动阶段
                self.window_size += 1
                print(f"慢启动阶段（Vegas），窗口大小增至：{self.window_size}")
            else:
                # 拥塞避免阶段，根据 diff 调整窗口
                if diff > self.beta:
                    self.window_size = max(self.window_size - 1, 1)
                    print(f"拥塞避免阶段（减小），窗口大小减至：{self.window_size}")
                elif diff < self.alpha:
                    self.window_size += 1
                    print(f"拥塞避免阶段（增大），窗口大小增至：{self.window_size}")
                else:
                    print(f"拥塞避免阶段（保持），窗口大小保持在：{self.window_size}")
        self.last_ack_num = ack_num

    def on_timeout(self, seq_num):
        # 超时处理
        self.ssthresh = max(self.window_size // 2, 2)
        self.window_size = 1
        self.duplicate_acks = 0
        self.base_rtt = None
        self.last_ack_num = -1
        print(f"发生超时（Vegas），调整 ssthresh={self.ssthresh}，窗口大小重置为 1")

    def get_window_size(self):
        return max(1, int(self.window_size))
