import os
import tkinter as tk
import paramiko
import pickle
from tkinter import messagebox
from tempfile import gettempdir

class RemoteManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Management Application")

        self.create_firewall_buttons()
        self.create_docker_buttons()

        self.load_window_state()

    def create_firewall_buttons(self):
        enable_button = tk.Button(self.root, text="Enable Firewall Rule", command=self.enable_firewall_rule)
        enable_button.pack(pady=10)

        disable_button = tk.Button(self.root, text="Disable Firewall Rule", command=self.disable_firewall_rule)
        disable_button.pack(pady=10)

    def create_docker_buttons(self):
        container_frame = tk.Frame(self.root)
        container_frame.pack(pady=20)

        start_button = tk.Button(container_frame, text="Start RTMP", command=self.start_docker_container, bg="green", fg="white", width=10, height=3)
        start_button.pack(side=tk.LEFT, padx=10)

        stop_button = tk.Button(container_frame, text="Stop RTMP", command=self.stop_docker_container, bg="red", fg="white", width=10, height=3)
        stop_button.pack(side=tk.LEFT, padx=10)

    #   restart_button = tk.Button(container_frame, text="Restart", command=self.restart_docker_services, bg="blue", fg="white", width=10, height=3)
    #   restart_button.pack(side=tk.LEFT, padx=10)

    #    status_button = tk.Button(container_frame, text="Status", command=self.check_docker_status, bg="purple", fg="white", width=10, height=3)
    #   status_button.pack(side=tk.LEFT, padx=10)

    def save_window_state(self):
        window_state = {
            'geometry': self.root.geometry(),
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y()
        }
        window_state_file = os.path.join(gettempdir(), 'window_state.pkl')
        with open(window_state_file, 'wb') as f:
            pickle.dump(window_state, f)

    def load_window_state(self):
        try:
            window_state_file = os.path.join(gettempdir(), 'window_state.pkl')
            with open(window_state_file, 'rb') as f:
                window_state = pickle.load(f)
                self.root.geometry(window_state['geometry'])
                self.root.geometry('+{}+{}'.format(window_state['x'], window_state['y']))
        except FileNotFoundError:
            pass

    def execute_ssh_commands(self, commands, success_message):
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

    def enable_firewall_rule(self):
        self.execute_ssh_commands("""
        config firewall policy
        edit 18
        set status enable
        next
        end
        """, "Firewall rule enabled")

    def disable_firewall_rule(self):
        self.execute_ssh_commands("""
        config firewall policy
        edit 18
        set status disable
        next
        end
        """, "Firewall rule disabled")

    def start_docker_container(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.0.205', username='root', password='q')

            ssh.exec_command('docker run -d -p 1935:1935 -p 8080:8080 alqutami/rtmp-hls')

            ssh.close()

            self.save_window_state()

            messagebox.showinfo("Success", "Started Docker container RTMP")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_docker_container(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.0.205', username='root', password='q')

            ssh.exec_command('''
                container_id=$(docker ps -q -f "ancestor=alqutami/rtmp-hls")
                if [ ! -z "$container_id" ]; then
                    docker stop "$container_id"
                    docker rm "$container_id"
                fi
            ''')

            ssh.close()

            self.save_window_state()

            messagebox.showinfo("Success", "Stopped Docker container RTMP")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def restart_docker_services(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.0.205', username='root', password='q')

            ssh.exec_command('''
                container_id=$(docker ps -q -f "ancestor=alqutami/rtmp-hls")
                if [ ! -z "$container_id" ]; then
                    docker restart "$container_id"
                fi
            ''')

            ssh.close()

            self.save_window_state()

            messagebox.showinfo("Success", "Restarted Docker services")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_docker_status(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.0.205', username='root', password='q')

            stdin, stdout, stderr = ssh.exec_command('docker ps -a')
            docker_status = stdout.read().decode()

            ssh.close()

            status_window = tk.Toplevel(self.root)
            status_window.title("Docker Container Status")

            status_text = tk.Text(status_window)
            status_text.pack()

            status_text.insert(tk.END, docker_status)

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoteManagementApp(root)
    root.mainloop()
