from mininet.topo import Topo
from mininet.net import Mininet

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import OVSController


class mytopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        Host1 = self.addHost("H1", ip="10.0.0.1", mac="00:00:00:00:ff:01")
        Host2 = self.addHost("H2", ip="10.0.0.2", mac="00:00:00:00:ff:02")
        Host3 = self.addHost("H3", ip="10.0.0.3", mac="00:00:00:00:ff:03")
        Host4 = self.addHost("H4", ip="10.0.0.4", mac="00:00:00:00:ff:04")
        Switch1 = self.addSwitch("S1")
        Switch2 = self.addSwitch("S2")

        self.addLink(Host1, Switch1, bw=10, delay="2ms")
        self.addLink(Host2, Switch1, bw=20, delay="10ms")
        self.addLink(Host3, Switch2, bw=10, delay="2ms")
        self.addLink(Host4, Switch2, bw=20, delay="10ms")
        self.addLink(Switch1, Switch2, bw=20, delay="2ms", loss=10)


def iperf(net, h1, h2):
    # net.ping([h1, h2]) # 测试连通性
    h2.cmd("iperf -s &")  # 在 H2 上启动 iperf 服务器
    result = h1.cmd("iperf -c " + h2.IP())  # 在 H1 上运行 iperf 客户端
    print("$ Iperf result:\n" + result)


def perfTest():
    topo = mytopo()
    net = Mininet(topo=topo, link=TCLink, controller=OVSController)
    net.start()
    # net.pingAll()
    h1, h2, h3, h4 = net.get("H1", "H2", "H3", "H4")

    iperf(net, h1, h2)
    iperf(net, h2, h4)
    iperf(net, h3, h4)

    # net.iperf((h1, h2))
    # net.iperf((h2, h4))
    # net.iperf((h3, h4))

    net.stop()


topos = {"mytopo": (lambda: mytopo())}

if __name__ == "__main__":
    setLogLevel("info")
    perfTest()
