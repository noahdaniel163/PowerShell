# Đường dẫn của thư mục chứa các tập tin shortcut
$folderPath = "E:\1"

# Lấy danh sách tất cả các tập tin shortcut trong thư mục
$shortcuts = Get-ChildItem -Path $folderPath -Filter *.lnk

# Duyệt qua từng shortcut và thay đổi đường dẫn mục tiêu
foreach ($shortcut in $shortcuts) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcutObject = $shell.CreateShortcut($shortcut.FullName)
    $targetPath = $shortcutObject.TargetPath
    
    # Kiểm tra nếu đường dẫn bắt đầu bằng "D:\"
    if ($targetPath -like "D:\*") {
        # Thay thế "D:\" bằng "E:\Software"
        $newTargetPath = $targetPath -replace "^D:\\", "E:\Software\"
        $shortcutObject.TargetPath = $newTargetPath
        $shortcutObject.Save()
        Write-Output "Thay đổi đường dẫn của shortcut $($shortcut.Name) thành $newTargetPath"
    }
}
