import ipaddress
import subprocess
import platform
from itertools import zip_longest
from tabulate import tabulate


def host_ping(address_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    reachable = []
    un_reachable = []
    for address in address_list:
        address = str(address)
        subproc_arg = ['ping', param, '1', address]
        response = subprocess.call(subproc_arg, stdout=subprocess.PIPE)
        if response == 0:
            print(f'{address} Узел доступен')
            reachable.append(address)
        else:
            print(f'{address} Узел не доступен')
            un_reachable.append(address)
    return zip_longest(reachable, un_reachable, fillvalue=None)


def host_range_ping(ip_addr, pos_dev):
    ip_address = ipaddress.ip_address(ip_addr)
    address_bytes = ip_addr.split('.')
    last_octet = address_bytes.pop()
    if int(last_octet) + pos_dev > 255:
        last_octet = '255'
    else:
        last_octet = str(int(last_octet) + pos_dev)
    address_bytes.append(last_octet)
    stop_ip_address = ipaddress.ip_address('.'.join(address_bytes))
    ip_addr_list = []
    while ip_address <= stop_ip_address:
        ip_addr_list.append(ip_address)
        ip_address += 1
    return host_ping(ip_addr_list)


def host_range_ping_tab(ip_addr, pos_dev):
    headers = ['reachable', 'un_reachable']
    table_body = host_range_ping(ip_addr, pos_dev)
    print(tabulate(table_body, headers=headers, tablefmt="grid"))


host_range_ping_tab('8.8.8.8', 3)
