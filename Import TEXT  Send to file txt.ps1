Add-Type -AssemblyName System.Windows.Forms

$form = New-Object System.Windows.Forms.Form
$form.Size = New-Object System.Drawing.Size(500,300)
$form.StartPosition = [System.Windows.Forms.FormStartPosition]::CenterScreen

$textbox = New-Object System.Windows.Forms.TextBox
$textbox.Size = New-Object System.Drawing.Size(450,200)
$textbox.Location = New-Object System.Drawing.Size(20,50)
$textbox.Multiline = $true
$form.Controls.Add($textbox)

$sendButton = New-Object System.Windows.Forms.Button
$sendButton.Size = New-Object System.Drawing.Size(75,23)
$sendButton.Location = New-Object System.Drawing.Point(375,270)
$sendButton.Text = "Send"
$sendButton.Add_Click({
    $text = $textbox.Text
    $time = Get-Date -Format "hh-mm-ss"
    $file = "E:\text $time.txt"
    Set-Content -Path $file -Value $text -Encoding "UTF8"
    $textbox.Clear()
})
$form.Controls.Add($sendButton)

$form.ShowDialog()
