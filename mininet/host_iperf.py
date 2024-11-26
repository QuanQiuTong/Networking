from mininet.topo import Topo
from mininet.net import Mininet

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import OVSController
import time
import threading


class MyTopo(Topo):
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
        self.addLink(Switch1, Switch2, bw=20, delay="2ms", loss=0)


topos = {"mytopo": (lambda: MyTopo())}


def iperf(h1, h2):
    h2.cmd("iperf -s &")
    result = h1.cmd("iperf -c " + h2.IP() + " -t 20 -i 0.5")
    print(result)


def perfTest2():
    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=OVSController)
    net.start()

    h1, h2, h3, h4 = net.get("H1", "H2", "H3", "H4")

    thread1 = threading.Thread(target=iperf, args=(h1, h3))
    thread2 = threading.Thread(target=iperf, args=(h2, h4))

    thread1.start()
    time.sleep(10)
    thread2.start()

    thread1.join()
    thread2.join()

    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    perfTest2()
