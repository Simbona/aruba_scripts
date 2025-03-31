## fiber uplinks

import pyaoscx.pyaoscx_module as pyaoscx
import concurrent.futures

def check_optical_power(switch_ip, username, password): #on one switch, given its address, username and passowrd
    try:
        test_switch = pyaoscx.PyAoscx(switch_ip, username, password)
        test_switch.api_version = 'v10.14' #adjust as needed.

        ports = ["1/1/49", "1/1/50"] #While all SFP ports (1/1/49-52) are uplinks, we typically use port 49 (primary) and 50 (secondary)
        power_levels = {}

        for port in ports:
            port_url = f"/interfaces/{port}"
            port_data = test_switch.get(port_url)

            if 'transceiver' in port_data and port_data['transceiver']:
                power_levels[port] = {
                    "rx_power": port_data['transceiver'].get('rx_power', 'N/A'),
                    "tx_power": port_data['transceiver'].get('tx_power', 'N/A'),
                }
            else:
                power_levels[port] = {"rx_power": "N/A", "tx_power": "N/A"}

        test_switch.close()
        return switch_ip, power_levels

    except pyaoscx.exceptions.AoscxResponseError as e:
        print(f"Error on {switch_ip}: {e}")
        return switch_ip, None
    except Exception as e:
        print(f"An unexpected error occurred on {switch_ip}: {e}")
        return switch_ip, None

def check_all_switches(switch_ip_list, username, password): #on a range of switches given a list of IPs
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_optical_power, ip, username, password) for ip in switch_ip_list]
        for future in concurrent.futures.as_completed(futures):
            switch_ip, power_levels = future.result()
            results[switch_ip] = power_levels

    for switch_ip, power_levels in results.items():
        print(f"\nSwitch: {switch_ip}")
        if power_levels:
            for port, levels in power_levels.items():
                print(f"  Port: {port}")
                print(f"    RX Power: {levels['rx_power']}")
                print(f"    TX Power: {levels['tx_power']}")
        else:
            print("  Failed to retrieve optical power levels.")

