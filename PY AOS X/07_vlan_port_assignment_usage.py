
from 07_vlan_port_assignment import get_vlan_info

switch_ip = "10.241.63.200"
username = "admin"
password = "@dm1.n"

vlan_data = get_vlan_info(switch_ip, username, password)

if vlan_data:
  for vlan_id, ports in vlan_data.items():
    print(f"Vlan {vlan_id} ports: {ports}") #print the ports and vlans assigned