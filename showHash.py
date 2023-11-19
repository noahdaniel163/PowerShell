import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import hashlib
import os

def calculate_hash():
    filepath = filedialog.askopenfilename()
    
    if filepath:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        
        hash_value = hasher.hexdigest()
        result_label.config(text=f"Hash: {hash_value}")
        copy_button.config(state=tk.NORMAL)
        export_button.config(state=tk.NORMAL)

def copy_hash():
    hash_value = result_label.cget("text").split(" ")[-1]
    root.clipboard_clear()
    root.clipboard_append(hash_value)
    root.update()
    messagebox.showinfo("Thông báo", "Đã sao chép mã hash vào clipboard!")

def export_hash():
    hash_value = result_label.cget("text").split(" ")[-1]
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if filepath:
        # Lấy tên tệp gốc
        original_filename = os.path.basename(filepath).split(".")[0]

        # Thêm "_Hash.txt" vào cuối
        new_filename = f"{original_filename}_Hash.txt"

        # Kết hợp đường dẫn thư mục và tên tệp mới
        new_filepath = os.path.join(os.path.dirname(filepath), new_filename)

        with open(new_filepath, 'w') as file:
            file.write(hash_value)
        messagebox.showinfo("Thông báo", f"Đã xuất mã hash vào tệp: {new_filepath}")

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Tính toán hash của tệp")

# Tạo nút chọn tệp và nút tính toán hash
select_button = tk.Button(root, text="Chọn tệp", command=calculate_hash)
select_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

# Tạo nút copy và nút export
copy_button = tk.Button(root, text="Copy", state=tk.DISABLED, command=copy_hash)
copy_button.pack(pady=5)

export_button = tk.Button(root, text="Export", state=tk.DISABLED, command=export_hash)
export_button.pack(pady=5)

# Khởi chạy giao diện
root.mainloop()
