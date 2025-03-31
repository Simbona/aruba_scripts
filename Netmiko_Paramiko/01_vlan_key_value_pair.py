## with this script, I will supply a key:value pair to configure ports and vlans
# example; 1/1/1:30 sets port 1/1/1 to vlan 30

from netmiko import ConnectHandler

def configure_switch(ip_address, username, pwd, port_and_vlan):

    # exception block handles potential issues like bad password
    try:
        device = {
            "device_type": "aruba_aoscx",
            "host": ip_address,
            "username": username,
            "password": pwd,
        }

        with ConnectHandler(**device) as net_connect:
            net_connect.enable()  # Enters enable mode

            config_commands = []
            for port_vlan in port_and_vlan.split(','):
                port, vlan = port_vlan.split(':')
                config_commands.append(f"interface {port}")
                config_commands.append(f"vlan access {vlan}")
                config_commands.append("exit")

            output = net_connect.send_config_set(config_commands)
            print(output)

    except Exception as e:
        print(f"An error occurred: {e}")
