import pyaoscx.pyaoscx_module as pyaoscx
import concurrent.futures
import json

def check_optical_power(switch_ip, username, password): #on one switch
    try:
        test_switch = pyaoscx.PyAoscx(switch_ip, username, password)
        test_switch.api_version = 'v10.04'  # Adjust as needed.

        ports = ["1/1/49", "1/1/50"]
        port_data = {}
        alarms = []

        system_url = "/system"
        system_data = test_switch.get(system_url)
        switch_name = system_data.get('hostname', 'N/A')

        for port in ports:
            port_url = f"/interfaces/{port}"
            interface_data = test_switch.get(port_url)

            port_data[port] = {
                "status": interface_data.get('admin_state', 'N/A'),
                "rx_power": 'N/A',
                "tx_power": 'N/A',
                "channel": 'N/A'
            }

            if 'transceiver' in interface_data and interface_data['transceiver']:
                transceiver_data = interface_data['transceiver']
                port_data[port]["rx_power"] = transceiver_data.get('rx_power', 'N/A')
                port_data[port]["tx_power"] = transceiver_data.get('tx_power', 'N/A')
                port_data[port]["channel"] = transceiver_data.get('channel', 'N/A')

        alarms_url = "/system/alarms"
        alarms_data = test_switch.get(alarms_url)
        if alarms_data and 'collection_result' in alarms_data:
            for alarm in alarms_data['collection_result']:
                alarms.append(alarm.get('description', 'Unknown alarm'))

        test_switch.close()
        return switch_ip, switch_name, port_data, alarms

    except pyaoscx.exceptions.AoscxResponseError as e:
        print(f"Error on {switch_ip}: {e}")
        return switch_ip, None, None, None
    except Exception as e:
        print(f"An unexpected error occurred on {switch_ip}: {e}")
        return switch_ip, None, None, None

def check_all_switches(switch_ips, username, password): #on a range of switches
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_optical_power, ip, username, password) for ip in switch_ips]
        for future in concurrent.futures.as_completed(futures):
            switch_ip, switch_name, port_data, alarms = future.result()
            results[switch_ip] = {
                "switch_name": switch_name,
                "ports": port_data,
                "alarms": alarms
            }

    json_output = {}
    for switch_ip, switch_data in results.items():
        json_output[switch_ip] = switch_data

    return json.dumps(json_output, indent=4)
