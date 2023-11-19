import os

folder_path = "E:\\1"
name_file_path = "E:\\name.txt"

# Đọc danh sách tên file từ tập tin name.txt
with open(name_file_path, "r") as file:
    name_list = file.read().splitlines()

# Đảm bảo thư mục chứa file tồn tại
if os.path.exists(folder_path):
    file_list = os.listdir(folder_path)
    renamed_files = []  # Danh sách các tên file đã được đổi tên
    
    for index, file_name in enumerate(file_list):
        if index >= len(name_list):
            break
        
        # Lấy tên mới từ danh sách tên file
        new_file_name = name_list[index]
        
        # Kiểm tra trùng lặp và thêm chữ "duplicate" nếu cần
        count = 1
        while new_file_name in renamed_files:
            base_name, extension = os.path.splitext(new_file_name)
            new_file_name = f"{base_name}_duplicate{count}{extension}"
            count += 1
        
        # Đường dẫn tới file cũ và file mới
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # Đổi tên file
        os.rename(old_file_path, new_file_path)
        
        renamed_files.append(new_file_name)
        
    print("Đổi tên file thành công!")
else:
    print("Thư mục không tồn tại.")
