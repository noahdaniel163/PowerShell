import tkinter as tk
from tkinter import messagebox
import paramiko

def enable_firewall_rule():
    execute_ssh_commands("""
    config firewall policy
    edit 18
    set status enable
    next
    end
    """, "Firewall rule enabled")

def disable_firewall_rule():
    execute_ssh_commands("""
    config firewall policy
    edit 18
    set status disable
    next
    end
    """, "Firewall rule disabled")

def execute_ssh_commands(commands, success_message):
    hostname = "192.168.0.1"
    port = 22
    username = "noah"
    password = "thanhbinh0316@B"

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname, port, username, password)
        stdin, stdout, stderr = ssh_client.exec_command(commands)
        output = stdout.read().decode()
        messagebox.showinfo("Success", success_message + "\n\n" + output)
    except paramiko.AuthenticationException:
        messagebox.showerror("Error", "Authentication failed")
    except paramiko.SSHException as e:
        messagebox.showerror("Error", "SSH error: " + str(e))
    finally:
        ssh_client.close()

# Tạo cửa sổ đồ hoạ với kích thước cụ thể
root = tk.Tk()
root.title("Firewall Rule Management")
root.geometry("342x241")  # Kích thước cửa sổ

# Tạo nút "Enable Firewall RULE"
enable_button = tk.Button(root, text="Enable Firewall RULE", command=enable_firewall_rule)
enable_button.pack(pady=10)

# Tạo nút "Disable Firewall RULE"
disable_button = tk.Button(root, text="Disable Firewall RULE", command=disable_firewall_rule)
disable_button.pack(pady=10)

# Bắt đầu vòng lặp sự kiện
root.mainloop()
