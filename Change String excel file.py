import os
from openpyxl import load_workbook

# Đường dẫn đến thư mục chứa file Excel
folder_path = r'E:\20230717'

# Lấy danh sách các file trong thư mục
file_list = os.listdir(folder_path)

for file_name in file_list:
    # Đường dẫn đầy đủ đến file
    file_path = os.path.join(folder_path, file_name)

    # Kiểm tra file có phải là file Excel hay không
    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        # Load file Excel
        workbook = load_workbook(file_path)

        # Chọn sheet đầu tiên
        sheet = workbook.active

        # Thay đổi giá trị ô C2
        if sheet['C2'].value:
            value = sheet['C2'].value
            parts = value.split('-')  # Tách chuỗi thành các phần

            if len(parts) == 6:
                parts[-1] = '01.xlsx'  # Thay đổi phần cuối thành '01.xlsx'

            new_value = '-'.join(parts)  # Ghép các phần thành chuỗi mới
            sheet['C2'] = new_value

        # Lưu file sau khi chỉnh sửa
        workbook.save(file_path)
        workbook.close()

        print(f"Đã chỉnh sửa file {file_name}")
