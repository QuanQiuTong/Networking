system-view
interface GigabitEthernet 0/0/0
ip address 192.168.1.254 24
interface GigabitEthernet 0/0/1
ip address 192.168.2.2 24

rip 1
network 192.168.1.0
network 192.168.2.0

display ip routing-table



system-view
interface GigabitEthernet 0/0/0
ip address 192.168.2.3 24
interface GigabitEthernet 0/0/1  
ip address 192.168.3.2 24

rip 1
network 192.168.2.0
network 192.168.3.0

display ip routing-table



system-view
interface GigabitEthernet 0/0/0
ip address 192.168.3.3 24
interface GigabitEthernet 0/0/1
ip address 192.168.4.254 24

rip 1
network 192.168.3.0
network 192.168.4.0

display ip routing-table
