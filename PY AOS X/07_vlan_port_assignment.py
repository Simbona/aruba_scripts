### Checks vlans and connected ports

import telnetlib
import re #for regular expressions to format data on vlans

def get_vlan_info(switch_ip, username, password):

    try:
        telnet_instance = telnetlib.Telnet(switch_ip)

        telnet_instance.read_until(b"Username: ")
        telnet_instance.write(username.encode('ascii') + b"\n")
        if password:
            telnet_instance.read_until(b"Password: ")
            telnet_instance.write(password.encode('ascii') + b"\n")

        telnet_instance.write(b"show vlan\n")
        telnet_instance.write(b"exit\n")

        output = telnet_instance.read_all().decode('ascii')
        telnet_instance.close()

        vlan_info = {}
        vlan_lines = re.findall(r"(\d+)\s+([\w-]+)\s+([\w\s,-]+)", output) #regular expressions retrieve vlan ID, name, and ports.

        for vlan_id, vlan_name, ports_str in vlan_lines:
            ports = [port.strip() for port in ports_str.split(',')]
            vlan_info[vlan_id] = ports

        print("VLAN Information:")
        for vlan_id, ports in vlan_info.items():
            print(f"  VLAN {vlan_id}: {len(ports)} ports")

        return vlan_info

    except Exception as e:
        print(f"Error: {e}")
        return None
