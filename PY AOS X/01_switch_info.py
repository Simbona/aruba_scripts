## SWITCH INFO BASED ON PYAOSCX

import pyaoscx.pyaoscx_module as pyaoscx
import json

def get_switch_info(switch_ip, username, password):

    try:
        test_switch = pyaoscx.PyAoscx(switch_ip, username, password)
        test_switch.api_version = 'v10.04' #Adjust as needed.

        # version and uptime
        system_info_url = "/system"
        system_info = test_switch.get(system_info_url)
        uptime = system_info['uptime']
        version = system_info['sw_version']

        # interface info and PoE
        interfaces_url = "/interfaces"
        interfaces_data = test_switch.get(interfaces_url)
        up_ports = []
        poe_ports = []
        non_poe_ports = []

        for interface in interfaces_data['collection_result']:
            int_name = interface['name']
            int_admin_state = interface['admin_state']
            int_oper_state = interface['oper_state']
            poe_status = interface.get('poe_status', None) #poe_status may be unavailable

            if int_admin_state == "up" and int_oper_state == "up":
                up_ports.append(int_name)
                if poe_status and poe_status["poe_enabled"]:
                  poe_ports.append(int_name)
                else:
                  non_poe_ports.append(int_name)

        # Print to output
        print(f"Switch IP: {switch_ip}")
        print(f"Uptime: {uptime}")
        print(f"Version: {version}")
        print("Up/Up Ports:", up_ports)
        print("PoE Ports:", poe_ports)
        print("Non-PoE Ports:", non_poe_ports)

        test_switch.close() #close connection.

    except pyaoscx.exceptions.AoscxResponseError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
