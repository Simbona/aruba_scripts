
from 04_uplink_optical_power import check_all_switches

switch_ips = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    # ... add all 50 switch IPs here
]
switch_ip = "10.241.63.200"
username = "admin"
password = "@dm1.n"

check_all_switches(switch_ips, username, password)