import socket
import os
from scapy.all import ARP, Ether, srp

def get_local_hostname():
    return socket.gethostname()

def get_mac_address(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=False)[0]

    if result:
        return result[0][1].hwsrc
    else:
        return "Not found"

def main():
    ip_address = input("Enter the IP address of the computer in the local network: ")

    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        hostname = "Not found"

    mac_address = get_mac_address(ip_address)

    print("Results:")
    print(f"IP Address: {ip_address}")
    print(f"Hostname: {hostname}")
    print(f"MAC Address: {mac_address}")

if __name__ == "__main__":
    main()
