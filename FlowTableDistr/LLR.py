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
from ryu.lib.packet import udp
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

        # x = 18  # 学号后两位
        # mod = lambda x: x % 16 if x % 16 != 0 else 16
        # src = '10.0.0.%d' % mod(x)
        # dst1 = '10.0.0.%d' % mod(x + 4)
        # dst2 = '10.0.0.%d' % mod(x + 5)

        # self.key = [(src, dst1), (src, dst2)]

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

    def cal_cost(self, path):
        max_load = 0
        for i in range(len(path) - 1):
            link = (path[i], path[i + 1])
            load = self.costs.get(link, 0)
            if load > max_load:
                max_load = load
        return max_load

    def cal_path(self, src, dst, src_port, dst_port):
        dpid1 = self.hosts[src][0]
        dpid2 = self.hosts[dst][0]

        key = (src, dst, src_port, dst_port)

        def max_link(dpid: int, ip1: str, ip2: str):
            return max(self.cal_cost(dpid, ip1), self.cal_cost(dpid, ip2))
        
        # 定义用于存储可能的路径及其最大链路负载的列表
        possible_paths = []

        # 如果两个主机连接在同一个交换机上
        if dpid1 == dpid2:
            path = [dpid1]
            max_load = self.cal_cost(path)
            possible_paths.append((max_load, path))
        else:
            # 获取所有可能的上行和下行端口组合
            uplinks = self.father[dpid1]
            downlinks = self.father[dpid2]

            # 获取所有可能的核心交换机
            core_switches = range(17, 21)

            # 遍历所有可能的路径，计算其最大链路负载
            for up in uplinks:
                for down in downlinks:
                    if up == down:
                        # 两个接入交换机连接到同一个汇聚交换机
                        path = [dpid1, up, dpid2]
                    else:
                        for core in core_switches:
                            path = [dpid1, up, core, down, dpid2]
                            max_load = self.cal_cost(path)
                            possible_paths.append((max_load, path))

        # 选择最大链路负载最小的路径
        if possible_paths:
            # 排序：首先按最大链路负载升序，其次按路径字典序升序（实现 LPR 原则）
            possible_paths.sort(key=lambda x: (x[0], x[1]))
            best_path = possible_paths[0][1]
        else:
            # 默认路径
            best_path = [dpid1, dpid2]

        # 更新链路负载信息
        for i in range(len(best_path) - 1):
            link = (best_path[i], best_path[i + 1])
            self.costs[link] += 1
            # 如果链路是双向的，可以同时更新反向链路
            reverse_link = (best_path[i + 1], best_path[i])
            self.costs[reverse_link] += 1

        # 存储计算得到的路径
        self.path[key] = best_path

        # 打印路径信息（可选）
        if self.cnt < 10:
            self.print_path(key)
            self.cnt += 1

    def get_nxt(self, dpid, src, dst, src_port, dst_port):
        key = (src, dst, src_port, dst_port)
        if key not in self.path:
            self.cal_path(src, dst, src_port, dst_port)
        now_path = self.path[key]
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

        # 忽略LLDP包
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return
        
        src = None
        dst = None
        src_port = None
        dst_port = None
        dpid = datapath.id
        match = None
        parser = datapath.ofproto_parser

        # 根据以太网类型处理IP包和ARP包
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            _ipv4 = pkt.get_protocol(ipv4.ipv4)
            src = _ipv4.src
            dst = _ipv4.dst

            if _ipv4.proto != ip.IPPROTO_UDP:
                print("Not UDP packet")
                return
            
            _udp = pkt.get_protocol(udp.udp)
            src_port = _udp.src_port
            dst_port = _udp.dst_port

            match = parser.OFPMatch(
                eth_type=ether_types.ETH_TYPE_IP,
                in_port=in_port,
                ipv4_src=src,
                ipv4_dst=dst,
                ip_proto=ip.IPPROTO_UDP,
                udp_src=_udp.src_port,
                udp_dst=_udp.dst_port,
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
            # 非IP或ARP包，直接返回
            return
        
        # 计算从当前交换机到目标主机的下一跳端口
        out_port = self.get_nxt(dpid, src, dst, src_port, dst_port)
        actions = [parser.OFPActionOutput(out_port)]

        # 安装流表项，避免后续相同的包再次触发packet_in
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, 1, match, actions)

        actions = [parser.OFPActionOutput(ofproto.OFPP_TABLE)]

        # 发送首包到指定端口
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:  # 还得把包送往该去的端口
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
