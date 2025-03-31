## Layer 2

import pyaoscx.pyaoscx_module as pyaoscx
import json

def get_layer2(switch_ip, username, password): # Retrieves ARP cache, MAC address table, and DHCP snooping data

    try:
        test_switch = pyaoscx.PyAoscx(switch_ip, username, password)
        test_switch.api_version = 'v10.14'

        # Get ARP cache
        arp_url = "/arp_entries"
        arp_data = test_switch.get(arp_url)

        # Get MAC address table
        mac_url = "/mac_address_table_entries"
        mac_data = test_switch.get(mac_url)

        # Get DHCP snooping binding table or statistics
        dhcp_url = "/dhcp_snooping/bindings" 
        dhcp_data = test_switch.get(dhcp_url)

        if not dhcp_data or 'collection_result' not in dhcp_data:
          dhcp_url = "/dhcp_snooping/statistics" #If bindings not available, try statistics.
          dhcp_data = test_switch.get(dhcp_url)

        # Print ARP cache
        print("\nARP Cache:")
        if arp_data and 'collection_result' in arp_data:
            for arp_entry in arp_data['collection_result']:
                print(f"  IP: {arp_entry['ip_address']}, MAC: {arp_entry['mac_address']}, Interface: {arp_entry.get('interface_name', 'N/A')}")
        else:
            print("  No ARP entries found.")

        # Print MAC address table
        print("\nMAC Address Table:")
        if mac_data and 'collection_result' in mac_data:
            for mac_entry in mac_data['collection_result']:
                print(f"  MAC: {mac_entry['mac_address']}, VLAN: {mac_entry['vlan_id']}, Interface: {mac_entry.get('interface_name', 'N/A')}")
        else:
            print("  No MAC address entries found.")

        # Print DHCP snooping data
        print("\nDHCP Snooping:")
        if dhcp_data and 'collection_result' in dhcp_data: #bindings
            for dhcp_binding in dhcp_data['collection_result']:
                print(f"  MAC: {dhcp_binding['mac_address']}, IP: {dhcp_binding['ip_address']}, VLAN: {dhcp_binding['vlan_id']}, Interface: {dhcp_binding.get('interface_name', 'N/A')}")
        elif dhcp_data and 'statistics' in dhcp_data: #statistics
            print(f"  Received Packets: {dhcp_data['statistics'].get('received_packets', 'N/A')}")
            print(f"  Dropped Packets: {dhcp_data['statistics'].get('dropped_packets', 'N/A')}")
            print(f"  Authorized Packets: {dhcp_data['statistics'].get('authorized_packets', 'N/A')}")
        else:
            print("  No DHCP snooping data found.")

        test_switch.close()
        return arp_data, mac_data, dhcp_data

    except pyaoscx.exceptions.AoscxResponseError as e:
        print(f"Error: {e}")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None, None
