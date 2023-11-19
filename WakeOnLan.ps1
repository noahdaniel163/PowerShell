$macAddress = "94-57-A5-ED-1F-8D"
$macBytes = $macAddress -split '-' | ForEach-Object { [byte]('0x' + $_) }
$magicPacket = @(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)

for ($i = 0; $i -lt 16; $i++) {
    $magicPacket += $macBytes
}

$udpClient = New-Object System.Net.Sockets.UdpClient
$udpClient.Connect(([System.Net.IPAddress]::Broadcast), 9)
$udpClient.Send($magicPacket, $magicPacket.Length)
$udpClient.Close()
