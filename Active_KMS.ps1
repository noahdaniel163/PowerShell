# Set the size of the console window
$rawUI = $Host.UI.RawUI
$newSize = $rawUI.BufferSize
$newSize.Height = 98
$newSize.Width = 8000
$rawUI.BufferSize = $newSize

# Create a graphical input box for the KMS server address
$kmsServer = Read-Host "Enter the KMS server address (default 42.116.30.117)" -Default "42.116.30.117"

# Prompt the user for the Activation Code
$ActivationCode = Read-Host "Enter the Activation code: W269N-WFGWX-YVC9B-4J6C9-T83GX for Windows 10 22H2 Pro"

# Run the license activation command
& "$env:windir\system32\slmgr.vbs" /skms $kmsServer
& "$env:windir\system32\slmgr.vbs" /ipk $ActivationCode
& "$env:windir\system32\slmgr.vbs" /ato

# Show the license status on the console
& "$env:windir\system32\slmgr.vbs" /dli
# Show the license status on the console
& "$env:windir\system32\slmgr.vbs" /xpr

# Wait for the user to press a key
Write-Host "If not activated, enter the license key manually in the graphical interface"
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
