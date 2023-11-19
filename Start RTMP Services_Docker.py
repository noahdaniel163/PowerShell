import os
import tkinter as tk
import paramiko
import pickle
from tkinter import messagebox
from tempfile import gettempdir

# Đường dẫn tới tập tin lưu trạng thái cửa sổ
window_state_file = os.path.join(gettempdir(), 'window_state.pkl')

def save_window_state(root):
    window_state = {
        'geometry': root.geometry(),
        'x': root.winfo_x(),
        'y': root.winfo_y()
    }
    with open(window_state_file, 'wb') as f:
        pickle.dump(window_state, f)

def load_window_state(root):
    try:
        with open(window_state_file, 'rb') as f:
            window_state = pickle.load(f)
            root.geometry(window_state['geometry'])
            root.geometry('+{}+{}'.format(window_state['x'], window_state['y']))
    except FileNotFoundError:
        pass

def start_docker_container():
    try:
        # Tạo kết nối SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.0.205', username='root', password='q')

        # Thực hiện lệnh bash shell từ xa để khởi động Docker container
        ssh.exec_command('docker run -d -p 1935:1935 -p 8080:8080 alqutami/rtmp-hls')

        # Đóng kết nối SSH
        ssh.close()

        # Lưu trạng thái cửa sổ trước khi đóng giao diện
        save_window_state(root)

        messagebox.showinfo("Thành công", "Đã bắt đầu Docker container RTMP")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def stop_docker_container():
    try:
        # Tạo kết nối SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.0.205', username='root', password='q')

        # Thực hiện lệnh bash shell từ xa để dừng Docker container
        ssh.exec_command('''
            container_id=$(docker ps -q -f "ancestor=alqutami/rtmp-hls")
            if [ ! -z "$container_id" ]; then
                docker stop "$container_id"
                docker rm "$container_id"
            fi
        ''')

        # Đóng kết nối SSH
        ssh.close()

        # Lưu trạng thái cửa sổ trước khi đóng giao diện
        save_window_state(root)

        messagebox.showinfo("Thành công", "Đã dừng Docker container RTMP")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Tạo giao diện đồ hoạ
root = tk.Tk()
root.title("Quản lý Docker container RTMP từ xa")

start_button = tk.Button(root, text="Bắt đầu", command=start_docker_container, bg="green", fg="white", width=10, height=3)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Dừng", command=stop_docker_container, bg="red", fg="white", width=10, height=3)
stop_button.pack(pady=10)

# Tải trạng thái cửa sổ
load_window_state(root)

root.mainloop()
