Add-Type -AssemblyName System.Windows.Forms

# Tạo cửa sổ và các thành phần giao diện
$mainForm = New-Object System.Windows.Forms.Form
$mainForm.Text = "Lấy ngày ngẫu nhiên"
$mainForm.Width = 400
$mainForm.Height = 200
$mainForm.StartPosition = "CenterScreen"
$mainForm.FormBorderStyle = "FixedDialog"
$mainForm.MaximizeBox = $false

$labelMonth = New-Object System.Windows.Forms.Label
$labelMonth.Text = "Tháng:"
$labelMonth.Location = New-Object System.Drawing.Point(20, 20)
$labelMonth.AutoSize = $true

$comboBoxMonth = New-Object System.Windows.Forms.ComboBox
$comboBoxMonth.Location = New-Object System.Drawing.Point(150, 20)
$comboBoxMonth.Size = New-Object System.Drawing.Size(50, 20)

# Thêm các mục vào menu thả xuống
$months = 1..12 | ForEach-Object { $_.ToString() }
$comboBoxMonth.Items.AddRange($months)

$labelYear = New-Object System.Windows.Forms.Label
$labelYear.Text = "Năm:"
$labelYear.Location = New-Object System.Drawing.Point(20, 50)
$labelYear.AutoSize = $true

$textYear = New-Object System.Windows.Forms.TextBox
$textYear.Location = New-Object System.Drawing.Point(150, 50)
$textYear.Size = New-Object System.Drawing.Size(50, 20)

$buttonGenerate = New-Object System.Windows.Forms.Button
$buttonGenerate.Text = "Tạo ngày ngẫu nhiên"
$buttonGenerate.Location = New-Object System.Drawing.Point(150, 90)
$buttonGenerate.Size = New-Object System.Drawing.Size(150, 30)

$mainForm.Controls.Add($labelMonth)
$mainForm.Controls.Add($comboBoxMonth)
$mainForm.Controls.Add($labelYear)
$mainForm.Controls.Add($textYear)
$mainForm.Controls.Add($buttonGenerate)

# Xử lý sự kiện khi nhấp vào nút "Tạo ngày ngẫu nhiên"
$buttonGenerate.Add_Click({
    $month = [int]$comboBoxMonth.SelectedItem
    $year = [int]$textYear.Text

    # Kiểm tra và điều chỉnh giá trị tháng và năm
    if ($month -lt 1 -or $month -gt 12) {
        [System.Windows.Forms.MessageBox]::Show("Tháng không hợp lệ. Vui lòng nhập lại!")
        return
    }
    if ($year -lt 1900 -or $year -gt 2100) {
        [System.Windows.Forms.MessageBox]::Show("Năm không hợp lệ. Vui lòng nhập lại!")
        return
    }

    # Tạo một mảng chứa tất cả các ngày trong tháng
    $daysInMonth = [System.DateTime]::DaysInMonth($year, $month)
    $dates = @()

    for ($day = 1; $day -le $daysInMonth; $day++) {
        $date = Get-Date -Year $year -Month $month -Day $day
        if ($date.DayOfWeek -ne 'Saturday' -and $date.DayOfWeek -ne 'Sunday') {
            $dates += $date.ToString("dd/MM/yyyy")
        }
    }

    # Lấy 40 ngày ngẫu nhiên từ mảng và sắp xếp chúng
    $randomDates = $dates | Get-Random -Count 40 | Sort-Object

    # Mở hộp thoại lưu file để người dùng chọn nơi lưu file
    $saveFileDialog = New-Object System.Windows.Forms.SaveFileDialog
    $saveFileDialog.Title = "Chọn vị trí lưu tệp tin"
    $saveFileDialog.Filter = "Tệp tin văn bản (*.txt)|*.txt"
    $saveFileDialog.InitialDirectory = [Environment]::GetFolderPath("MyDocuments")
    $saveFileDialog.FileName = "random_dates.txt"
    
    if ($saveFileDialog.ShowDialog() -eq 'OK') {
        $filePath = $saveFileDialog.FileName

        # Lưu kết quả vào tệp tin được chọn
        $randomDates | Out-File -FilePath $filePath

        # Hiển thị kết quả trong cửa sổ thông báo
        [System.Windows.Forms.MessageBox]::Show("Các ngày ngẫu nhiên đã được lưu vào tệp tin '$filePath':`n$($randomDates -join "`n")")
    }
})

# Hiển thị cửa sổ
[void]$mainForm.ShowDialog()
