
from 08_poe import get_port_poe_speed

switch_ip = "10.241.63.200"
username = "admin"
password = "@dm1.n"

port_data = get_port_poe_speed(switch_ip, username, password)