##This script checks traffic and statistics. It worked with CX 6100 but I had troubles with CX 6200


import pyaoscx.pyaoscx_module as pyaoscx
import json # I need this output to be nicely formatted as JSON

def get_stats(switch_ip, username, pwd):

    try:
        test_switch = pyaoscx.PyAoscx(switch_ip, username, pwd)
        test_switch.api_version = 'v10.14' #as of March 2025, latest in use is 10.14.1050

        # Get user sessions
        user_sessions_url = "/system/sessions"
        user_sessions_data = test_switch.get(user_sessions_url)

        interfaces_url = "/interfaces" #retrieves interface statistics like number of times it went up and down
        interfaces_data = test_switch.get(interfaces_url)

        user_info = {} #start with empty objects
        interface_traffic = {}

        # user sessions
        if user_sessions_data and 'collection_result' in user_sessions_data:
            for session in user_sessions_data['collection_result']:
                user_info[session['id']] = {
                    'username': session.get('username', 'N/A'),
                    'client_ip': session.get('client_ip', 'N/A'),
                }
        else:
            print("No user session data found.")

        # Process interface traffic
        if interfaces_data and 'collection_result' in interfaces_data:
            for interface in interfaces_data['collection_result']:
                interface_name = interface['name']
                interface_traffic[interface_name] = {
                    'in_octets': interface.get('statistics', {}).get('in_octets', 'N/A'),
                    'out_octets': interface.get('statistics', {}).get('out_octets', 'N/A'),
                }
        else:
            print("No interface traffic data found.")

        # Print user information
        print("\nUser Sessions:")
        for session_id, user_data in user_info.items():
            print(f"  Session ID: {session_id}")
            print(f"    Username: {user_data['username']}")
            print(f"    Client IP: {user_data['client_ip']}")

        # Print interface traffic
        print("\nInterface Traffic:")
        for interface_name, traffic_data in interface_traffic.items():
            print(f"  Interface: {interface_name}")
            print(f"    In Octets: {traffic_data['in_octets']}")
            print(f"    Out Octets: {traffic_data['out_octets']}")

        test_switch.close()
        return user_info, interface_traffic

    except pyaoscx.exceptions.AoscxResponseError as e:
        print(f"Error: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None
