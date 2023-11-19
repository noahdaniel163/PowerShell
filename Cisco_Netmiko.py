from netmiko import ConnectHandler

def get_network_id(ip_address, subnet_mask):
    ip_octets = [int(octet) for octet in ip_address.split('.')]
    subnet_octets = [int(octet) for octet in subnet_mask.split('.')]
    net_id = [str(ip_octets[i] & subnet_octets[i]) for i in range(4)]
    return '.'.join(net_id)

def main():
    cisco_device = {
        'device_type': 'cisco_ios',
        'ip': '10.210.102.209',  # Địa chỉ IP của router Cisco
        'username': 'admin',
        'password': 'busan',
    }

    # Kết nối đến router Cisco
    net_connect = ConnectHandler(**cisco_device)

    # Lấy thông tin địa chỉ IP và subnet mask từ router
    show_ip_interface_brief = net_connect.send_command('show ip interface brief')
    for line in show_ip_interface_brief.splitlines():
        if 'Ethernet' in line:  # Điều chỉnh tên giao diện của router nếu cần thiết
            _, interface, _, ip_address, _, _, _, subnet_mask = line.split()
            break

    # Xác định Net ID của mạng LAN
    net_id = get_network_id(ip_address, subnet_mask)

    # Địa chỉ IP cần kiểm tra
    target_ip = '10.210.102.209'

    # Xác định Net ID của địa chỉ IP cần kiểm tra
    target_net_id = get_network_id(target_ip, subnet_mask)

    # So sánh Net ID
    if net_id == target_net_id:
        print(f"Địa chỉ IP {target_ip} nằm trong cùng mạng LAN với router Cisco.")
    else:
        print(f"Địa chỉ IP {target_ip} không nằm trong cùng mạng LAN với router Cisco.")

if __name__ == "__main__":
    main()
