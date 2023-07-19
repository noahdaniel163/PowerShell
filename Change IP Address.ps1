Add-Type -AssemblyName System.Windows.Forms

# Tạo form và các thành phần
$form = New-Object System.Windows.Forms.Form
$labelAdapter = New-Object System.Windows.Forms.Label
$dropdownAdapter = New-Object System.Windows.Forms.ComboBox
$labelIP = New-Object System.Windows.Forms.Label
$textboxIP = New-Object System.Windows.Forms.TextBox
$labelSubnet = New-Object System.Windows.Forms.Label
$textboxSubnet = New-Object System.Windows.Forms.TextBox
$labelGateway = New-Object System.Windows.Forms.Label
$textboxGateway = New-Object System.Windows.Forms.TextBox
$button = New-Object System.Windows.Forms.Button

$form.Text = "Thay đổi cấu hình mạng"
$form.Size = New-Object System.Drawing.Size(400, 300)

$labelAdapter.Text = "Chọn card mạng:"
$labelAdapter.Location = New-Object System.Drawing.Point(10, 20)
$labelAdapter.AutoSize = $true

$dropdownAdapter.Location = New-Object System.Drawing.Point(10, 50)
$dropdownAdapter.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList

$labelIP.Text = "Địa chỉ IP:"
$labelIP.Location = New-Object System.Drawing.Point(10, 90)
$labelIP.AutoSize = $true

$textboxIP.Location = New-Object System.Drawing.Point(120, 90)
$textboxIP.Size = New-Object System.Drawing.Size(200, 20)

$labelSubnet.Text = "Subnet Mask:"
$labelSubnet.Location = New-Object System.Drawing.Point(10, 130)
$labelSubnet.AutoSize = $true

$textboxSubnet.Location = New-Object System.Drawing.Point(120, 130)
$textboxSubnet.Size = New-Object System.Drawing.Size(200, 20)

$labelGateway.Text = "Default Gateway:"
$labelGateway.Location = New-Object System.Drawing.Point(10, 170)
$labelGateway.AutoSize = $true

$textboxGateway.Location = New-Object System.Drawing.Point(120, 170)
$textboxGateway.Size = New-Object System.Drawing.Size(200, 20)

$button.Text = "Thay đổi"
$button.Location = New-Object System.Drawing.Point(10, 210)
$button.Add_Click({
    $selectedAdapter = $dropdownAdapter.SelectedItem
    $ipAddress = $textboxIP.Text
    $subnetMask = $textboxSubnet.Text
    $gateway = $textboxGateway.Text

    # Lấy thông tin card mạng được chọn
    $adapter = Get-WmiObject -Class Win32_NetworkAdapterConfiguration | Where-Object { $_.Description -eq $selectedAdapter }
    if ($adapter -ne $null) {
        # Thực hiện thay đổi cấu hình mạng
        $adapter.EnableStatic($ipAddress, $subnetMask)
        $adapter.SetGateways($gateway)
    }

    # Hiển thị thông báo
    $message = "Đã thay đổi cấu hình mạng cho $selectedAdapter."
    [System.Windows.Forms.MessageBox]::Show($message)
})

# Lấy danh sách các card mạng và thêm vào dropdown
$adapters = Get-WmiObject -Class Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true }
foreach ($adapter in $adapters) {
    $dropdownAdapter.Items.Add($adapter.Description)
}

# Thêm các thành phần vào form
$form.Controls.Add($labelAdapter)
$form.Controls.Add($dropdownAdapter)
$form.Controls.Add($labelIP)
$form.Controls.Add($textboxIP)
$form.Controls.Add($labelSubnet)
$form.Controls.Add($textboxSubnet)
$form.Controls.Add($labelGateway)
$form.Controls.Add($textboxGateway)
$form.Controls.Add($button)

[void]$form.ShowDialog()
Thay vì hiển thị tên card mạng hảy hiển thị Adapter Name