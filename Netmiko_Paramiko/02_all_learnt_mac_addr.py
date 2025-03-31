### using netmiko to collect all mac addresses from a switch

import asyncio
import pysnmp.hlapi.asyncio as hlapi
import ipaddress

async def get_mac_addr(host, community='marriott', port=161): #uses SNMP, community is Marriott

    mac_addresses = {}

    try:
        g = hlapi.getCmd(
            hlapi.SnmpEngine(),
            hlapi.CommunityData(community),
            hlapi.UdpTransportTarget((host, port)),
            hlapi.ContextData(),
            hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.2.1.17.4.3.1.1')),  ''' This is the SNMP OID for "A unicast MAC address for which the bridge has
forwarding and/or filtering information." '''
            lookupMib=False,
        )

        async for (errorIndication, errorStatus, errorIndex, varBinds) in g:
            if errorIndication:
                print(f'SNMP Error: {errorIndication}')
                return None

            if errorStatus:
                print(f'SNMP Error: {errorStatus.prettyPrint()}')
                return None

            for varBind in varBinds:
                oid, value = varBind
                mac_address = ':'.join(f'{byte:02x}' for byte in value)
                if_index_oid = oid.parent() + '.2.' + oid.getComponentByPosition(8).prettyPrint() 
                g2 = hlapi.getCmd(
                  hlapi.SnmpEngine(),
                  hlapi.CommunityData(community),
                  hlapi.UdpTransportTarget((host, port)),
                  hlapi.ContextData(),
                  hlapi.ObjectType(hlapi.ObjectIdentity(if_index_oid)),
                  lookupMib=False,
                )
                async for (errorIndication2, errorStatus2, errorIndex2, varBinds2) in g2:
                  if errorIndication2:
                    interface_name = "unknown"
                  elif errorStatus2:
                    interface_name = "unknown"
                  else:
                    for varBind2 in varBinds2:
                      interface_name = varBind2[1].prettyPrint()

                mac_addresses[mac_address] = interface_name

        return mac_addresses

    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return None

async def main(host, community='public', port=161):
    mac_data = await get_mac_addr(host, community, port)

    if mac_data:
        print('MAC Addresses:')
        for mac, interface in mac_data.items():
            print(f'  {mac}: {interface}')

if __name__ == '__main__':
    host = '10.241.63.200'  
    community = 'marriott' 
    port = 161  # UDP port for SNMP

    asyncio.run(main(host, community, port))