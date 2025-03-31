
from 06_layer2 import get_layer2

switch_ip = "your_switch_ip"
username = "your_username"
password = "your_password"

arp_data, mac_data, dhcp_data = get_layer2(switch_ip, username, password)