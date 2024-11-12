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


class RenoCongestionControl(CongestionControl):
    def __init__(self):
        self.window_size = 1
        self.ssthresh = 64
        self.duplicate_acks = 0

    def on_ack_received(self, ack_num, rtt):
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


class VegasCongestionControl(CongestionControl):
    def __init__(self):
        self.window_size = 1
        self.ssthresh = 64
        self.base_rtt = float("inf")
        self.alpha = 1
        self.beta = 3
        self.duplicate_acks = 0

    def on_ack_received(self, ack_num, rtt):
        self.base_rtt = min(self.base_rtt, rtt)
        expected_rate = self.window_size / self.base_rtt
        actual_rate = self.window_size / rtt
        diff = expected_rate - actual_rate

        if self.window_size < self.ssthresh:
            self.window_size += 1  # 慢启动阶段
        else:
            if diff > self.beta:
                self.window_size -= 1  # 拥塞避免阶段，减少窗口
            elif diff < self.alpha:
                self.window_size += 1  # 拥塞避免阶段，增加窗口

        self.duplicate_acks = 0

    def on_timeout(self, seq_num):
        self.ssthresh = max(self.window_size // 2, 1)
        self.window_size = 1
        self.duplicate_acks = 0

    def get_window_size(self):
        return self.window_size
