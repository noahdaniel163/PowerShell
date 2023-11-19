from scapy.all import ARP, Ether, srp, conf
import socket

def scan(ip):
    conf.L3socket = conf.L3socket6

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def get_hostnames(ip_addresses):
    hostnames = []
    for ip in ip_addresses:
        try:
            hostname = socket.gethostbyaddr(ip)
            hostnames.append({'ip': ip, 'hostname': hostname[0]})
        except socket.herror:
            hostnames.append({'ip': ip, 'hostname': "N/A"})
    return hostnames

# Người dùng nhập netid
netid = input("Nhập netid (ví dụ: 192.168.1.0/24): ")

devices = scan(netid)

for device in devices:
    try:
        hostnames = get_hostnames([device['ip']])
        device['hostname'] = hostnames[0]['hostname']
    except Exception as e:
        device['hostname'] = "N/A"

for device in devices:
    print(f"IP: {device['ip']}   MAC: {device['mac']}   Hostname: {device['hostname']}")
