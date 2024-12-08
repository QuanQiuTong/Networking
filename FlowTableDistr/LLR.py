from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import arp
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import ether_types
from ryu.lib import mac, ip
from ryu.topology import event
from collections import defaultdict


class ProjectController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ProjectController, self).__init__(*args, **kwargs)
        self.datapath_list = {}
        self.switches = []
        self.adjacency = defaultdict(dict)
        self.hosts = {'10.0.0.1': (1, 1), '10.0.0.2': (1, 2), '10.0.0.3': (2, 1), '10.0.0.4': (2, 2),
                      '10.0.0.5': (3, 1), '10.0.0.6': (3, 2), '10.0.0.7': (4, 1), '10.0.0.8': (4, 2),
                      '10.0.0.9': (5, 1), '10.0.0.10': (5, 2), '10.0.0.11': (6, 1), '10.0.0.12': (6, 2),
                      '10.0.0.13': (7, 1), '10.0.0.14': (7, 2), '10.0.0.15': (8, 1), '10.0.0.16': (8, 2)}
        self.father = {1: (9, 10), 2: (9, 10), 3: (11, 12), 4: (11, 12), 5: (13, 14), 6: (13, 14), 7: (15, 16), 8: (15, 16),
                       9: (17, 18), 10: (19, 20), 11: (17, 18), 12: (19, 20), 13: (17, 18), 14: (19, 20), 15: (17, 18), 16: (19, 20)}
        self.ip_son = {
            9: {"10.0.0.1": 1, "10.0.0.2": 1, "10.0.0.3": 2, "10.0.0.4": 2},
            10: {"10.0.0.1": 1, "10.0.0.2": 1, "10.0.0.3": 2, "10.0.0.4": 2},
            11: {"10.0.0.5": 3, "10.0.0.6": 3, "10.0.0.7": 4, "10.0.0.8": 4},
            12: {"10.0.0.5": 3, "10.0.0.6": 3, "10.0.0.7": 4, "10.0.0.8": 4},
            13: {"10.0.0.9": 5, "10.0.0.10": 5, "10.0.0.11": 6, "10.0.0.12": 6},
            14: {"10.0.0.9": 5, "10.0.0.10": 5, "10.0.0.11": 6, "10.0.0.12": 6},
            15: {"10.0.0.13": 7, "10.0.0.14": 7, "10.0.0.15": 8, "10.0.0.16": 8},
            16: {"10.0.0.13": 7, "10.0.0.14": 7, "10.0.0.15": 8, "10.0.0.16": 8},
            17: {
                "10.0.0.1": 9,
                "10.0.0.2": 9,
                "10.0.0.3": 9,
                "10.0.0.4": 9,
                "10.0.0.5": 11,
                "10.0.0.6": 11,
                "10.0.0.7": 11,
                "10.0.0.8": 11,
                "10.0.0.9": 13,
                "10.0.0.10": 13,
                "10.0.0.11": 13,
                "10.0.0.12": 13,
                "10.0.0.13": 15,
                "10.0.0.14": 15,
                "10.0.0.15": 15,
                "10.0.0.16": 15,
            },
            18: {
                "10.0.0.1": 9,
                "10.0.0.2": 9,
                "10.0.0.3": 9,
                "10.0.0.4": 9,
                "10.0.0.5": 11,
                "10.0.0.6": 11,
                "10.0.0.7": 11,
                "10.0.0.8": 11,
                "10.0.0.9": 13,
                "10.0.0.10": 13,
                "10.0.0.11": 13,
                "10.0.0.12": 13,
                "10.0.0.13": 15,
                "10.0.0.14": 15,
                "10.0.0.15": 15,
                "10.0.0.16": 15,
            },
            19: {
                "10.0.0.1": 10,
                "10.0.0.2": 10,
                "10.0.0.3": 10,
                "10.0.0.4": 10,
                "10.0.0.5": 12,
                "10.0.0.6": 12,
                "10.0.0.7": 12,
                "10.0.0.8": 12,
                "10.0.0.9": 14,
                "10.0.0.10": 14,
                "10.0.0.11": 14,
                "10.0.0.12": 14,
                "10.0.0.13": 16,
                "10.0.0.14": 16,
                "10.0.0.15": 16,
                "10.0.0.16": 16,
            },
            20: {
                "10.0.0.1": 10,
                "10.0.0.2": 10,
                "10.0.0.3": 10,
                "10.0.0.4": 10,
                "10.0.0.5": 12,
                "10.0.0.6": 12,
                "10.0.0.7": 12,
                "10.0.0.8": 12,
                "10.0.0.9": 14,
                "10.0.0.10": 14,
                "10.0.0.11": 14,
                "10.0.0.12": 14,
                "10.0.0.13": 16,
                "10.0.0.14": 16,
                "10.0.0.15": 16,
                "10.0.0.16": 16,
            },
        }
        self.costs = defaultdict(int)
        self.cnt = 0
        self.path = defaultdict(list)

        x = 18  # 学号后两位
        mod = lambda x: x % 16 if x % 16 != 0 else 16
        src = '10.0.0.%d' % mod(x)
        dst1 = '10.0.0.%d' % mod(x + 4)
        dst2 = '10.0.0.%d' % mod(x + 5)

        self.key = [(src, dst1), (src, dst2)]

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def cal_cost(self, dpid: int, ip: str):
        if self.hosts[ip][0] == dpid:
            return 0
        ans = 0
        while self.hosts[ip][0] != dpid:
            son = self.ip_son[dpid][ip]
            ans = max(ans, self.costs[(dpid, son)])
            dpid = son
        return ans

    def cal_path(self, src, dst):
        dpid1 = self.hosts[src][0]
        dpid2 = self.hosts[dst][0]

        def max_link(dpid: int, ip1: str, ip2: str):
            return max(self.cal_cost(dpid, ip1), self.cal_cost(dpid, ip2))
        
        if dpid1 == dpid2:
            self.path[(src, dst)] = [dpid1]
        elif self.father[dpid1] == self.father[dpid2]:
            fa = self.father[dpid1]
            # 负载相同时选择左边的路径(fa[0])
            chosen_father = fa[0] if max_link(fa[0], src, dst) <= max_link(fa[1], src, dst) else fa[1]
            self.path[(src, dst)] = [dpid1, chosen_father, dpid2]
        else:
            mindpid = min(range(17, 21), key=lambda i: max_link(i, src, dst))
            self.path[(src, dst)] = [
                dpid1,
                self.ip_son[mindpid][src],
                mindpid,
                self.ip_son[mindpid][dst],
                dpid2,
            ]

        now_path = self.path[(src, dst)]
        for i in range(len(now_path) - 1):
            self.costs[(now_path[i], now_path[i + 1])] += 1
            self.costs[(now_path[i + 1], now_path[i])] += 1
        if self.cnt < 10:
            self.print_path((src, dst))
            self.cnt += 1

    def get_nxt(self, dpid, src, dst):
        if (src, dst) not in self.path:
            self.cal_path(src, dst)
        now_path = self.path[(src, dst)]
        for i in range(len(now_path)):
            if now_path[i] == dpid:
                if i == len(now_path) - 1:
                    return self.hosts[dst][1]
                try:
                    return self.adjacency[dpid][now_path[i + 1]]
                except KeyError:
                    return ofproto_v1_3.OFPP_FLOOD
        return ofproto_v1_3.OFPP_FLOOD

    def print_path(self, key):
        ip2num = lambda x: int(x.split(".")[-1])
        print("h%d ->" % (ip2num(key[0])), end=" ")
        for i in self.path[key]:
            print("s%d ->" % (i), end=" ")
        print("h%d" % (ip2num(key[1])))

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        print("switch_features_handler is called")
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        in_port = msg.match["in_port"]
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return
        src = None
        dst = None
        dpid = datapath.id
        match = None
        parser = datapath.ofproto_parser
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            _ipv4 = pkt.get_protocol(ipv4.ipv4)
            src = _ipv4.src
            dst = _ipv4.dst
            match = parser.OFPMatch(
                eth_type=ether_types.ETH_TYPE_IP,
                in_port=in_port,
                ipv4_src=src,
                ipv4_dst=dst,
            )
        elif eth.ethertype == ether_types.ETH_TYPE_ARP:
            arp_pkt = pkt.get_protocol(arp.arp)
            src = arp_pkt.src_ip
            dst = arp_pkt.dst_ip
            match = parser.OFPMatch(
                eth_type=ether_types.ETH_TYPE_ARP,
                in_port=in_port,
                arp_spa=src,
                arp_tpa=dst,
            )
        else:
            return
        out_port = self.get_nxt(dpid, src, dst)
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        print(ev)
        switch = ev.switch.dp
        if switch.id not in self.switches:
            self.switches.append(switch.id)
            self.datapath_list[switch.id] = switch

    @set_ev_cls(event.EventSwitchLeave, MAIN_DISPATCHER)
    def switch_leave_handler(self, ev):
        print(ev)
        switch = ev.switch.dp.id
        if switch in self.switches:
            self.switches.remove(switch)
            del self.datapath_list[switch]
            del self.adjacency[switch]

    # get adjacency matrix of fattree
    @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
    def link_add_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        self.adjacency[s1.dpid][s2.dpid] = s1.port_no
        self.adjacency[s2.dpid][s1.dpid] = s2.port_no
        # 初始化链路负载
        self.costs[(s1.dpid,s2.dpid)] = 0
        self.costs[(s2.dpid,s1.dpid)] = 0

    @set_ev_cls(event.EventLinkDelete, MAIN_DISPATCHER)
    def link_delete_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        # Exception handling if switch already deleted
        try:
            del self.adjacency[s1.dpid][s2.dpid]
            del self.adjacency[s2.dpid][s1.dpid]
        except KeyError:
            pass
