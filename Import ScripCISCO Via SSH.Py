import pexpect

# Tạo kết nối SSH
child = pexpect.spawn('ssh -1 admin@10.210.102.209')

# Đợi prompt mật khẩu và gửi mật khẩu
child.expect('password:')
child.sendline('busan')

# Đọc nội dung từ file txt
with open('E:/1.txt', 'r') as file:
    commands = file.readlines()

# Thực hiện nhập các lệnh
for command in commands:
    child.sendline(command.strip())
    child.expect('#')

# Đóng kết nối
child.sendline('exit')
