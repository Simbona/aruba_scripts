
from 03_device_use_traffic import get_stats

switch_ip = "10.241.63.200"
username = "admin"
password = "@dm1.n"

user_data, traffic_data = get_stats(switch_ip, username, password)