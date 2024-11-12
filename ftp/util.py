import hashlib


def file_md5(file_path) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


from ftpsender import Sender
from ftpreceiver import GBNReceiver, SRReceiver


def upload(filename, socket, addr, protocol):
    with open(filename, "rb") as f:
        data = f.read()
        print(f"成功读取文件，文件大小：{len(data)} 字节")
    sender = Sender(socket, addr, retransmission=protocol)
    sender.start(data)

    # 计算文件的MD5哈希值
    md5_hash = file_md5(filename)
    socket.sendto(md5_hash.encode(), addr)


def download(filename, socket, protocol, prefix="download_"):
    if protocol == "GBN":
        receiver = GBNReceiver(socket)
    elif protocol == "SR":
        receiver = SRReceiver(socket)
    else:
        raise ValueError("Invalid protocol")
    
    receiver.start()
    with open(prefix + filename, "wb") as f:
        f.write(receiver.file_data)
        print(f"成功写入文件，文件大小：{len(receiver.file_data)} 字节")
        
    # 计算文件的MD5哈希值
    md5_hash, _ = socket.recvfrom(1024)
    if md5_hash.decode() == file_md5(prefix + filename):
        print("文件校验正确")
    else:
        print("文件校验错误")
