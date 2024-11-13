from ftpsender import Sender
from ftpreceiver import GBNReceiver, SRReceiver

def upload(filename, socket, addr, protocol):
    with open(filename, "rb") as f:
        data = f.read()
        print(f"成功读取文件，文件大小：{len(data)} 字节")

    sender = Sender(socket, addr, retransmission=protocol)
    sender.start(data)


def download(filename, socket, protocol, prefix="download_"):
    if protocol == "GBN":
        receiver = GBNReceiver(socket, prefix + filename)
    elif protocol == "SR":
        receiver = SRReceiver(socket, prefix + filename)
    else:
        raise ValueError("Invalid protocol")

    receiver.start()
    # 文件保存和MD5校验已经在接收器中处理，不需要在此重复处理