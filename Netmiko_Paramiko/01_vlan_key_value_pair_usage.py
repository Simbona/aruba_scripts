# Usage

from 01_vlan_key_value_pair import configure_switch

switch_ip = "10.241.63.200"
username = "admin"
password = "@dm1.n"
port_vlan_map = "1/1/1:20,1/1/2:40,1/1/3:99"

configure_switch(switch_ip, username, password, port_vlan_map)