
from 05_optical_power_json import check_all_switches

username = "your_username"
password = "your_password"

switch_ips = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12"
]

json_result = check_all_switches(switch_ips, username, password)
print(json_result)