
import pyaoscx.pyaoscx_module as pyaoscx
import json

def get_port_poe_speed(switch_ip, username, password):

    try:
        sw = pyaoscx.PyAoscx(switch_ip, username, password)
        sw.api_version = 'v10.14' 

        interfaces_url = "/interfaces"
        interfaces_data = sw.get(interfaces_url)

        port_info = {}

        for interface in interfaces_data['collection_result']:
            int_name = interface['name']
            port_info[int_name] = {}
            if 'poe_status' in interface and interface['poe_status'] and interface['poe_status']['poe_enabled']:
                poe_status = interface['poe_status']
                port_info[int_name]['poe_power'] = poe_status.get('power_allocated', 'N/A')
                port_info[int_name]['poe_status'] = poe_status.get('power_status', 'N/A')
            else:
                port_info[int_name]['poe_power'] = "N/A"
                port_info[int_name]['poe_status'] = "N/A"

            if 'oper_speed' in interface:
                port_info[int_name]['oper_speed'] = interface['oper_speed']
            else:
                port_info[int_name]['oper_speed'] = "N/A"

        print("Port PoE and Speed Information:")
        for port, info in port_info.items():
            print(f"  Port: {port}")
            print(f"    PoE Power: {info['poe_power']}")
            print(f"    PoE Status: {info['poe_status']}")
            print(f"    Operating Speed: {info['oper_speed']}")

        sw.close()
        return port_info

    except pyaoscx.exceptions.AoscxResponseError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


