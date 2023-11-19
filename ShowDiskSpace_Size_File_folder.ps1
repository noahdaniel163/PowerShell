$largeFiles = @{}
$directorySizes = @{}

$allFiles = Get-ChildItem -Path C:\ -Recurse -File -ErrorAction SilentlyContinue
foreach ($file in $allFiles) {
    try {
        if ($file.Length -gt 100MB) {
            $largeFiles[$file.FullName] = $file
        }
    } catch {
    }
}

$excel = New-Object -ComObject Excel.Application
$workbook = $excel.Workbooks.Add()
$sheet = $workbook.Worksheets.Add()

$sheet.Cells.Item(1,1) = "Tên tập tin"
$sheet.Cells.Item(1,2) = "Đường dẫn tập tin"
$sheet.Cells.Item(1,3) = "Dung lượng (GB)"

$row = 2
$totalSize = 0
foreach ($file in $largeFiles.Values) {
    $sheet.Cells.Item($row, 1) = $file.Name
    $sheet.Cells.Item($row, 2) = $file.FullName
    $sizeGB = [math]::Round($file.Length / 1GB, 2)
    $sheet.Cells.Item($row, 3) = $sizeGB
    $totalSize += $sizeGB
    $row++

    $parentPath = $file.Directory.FullName
    while ($parentPath -ne "C:\") {
        if ($directorySizes.ContainsKey($parentPath)) {
            $directorySizes[$parentPath] += $sizeGB
        } else {
            $directorySizes[$parentPath] = $sizeGB
        }
        $parentPath = (Get-Item $parentPath).Parent.FullName
    }
}

$sheet.Cells.Item($row, 2) = "Tổng dung lượng:"
$sheet.Cells.Item($row, 3) = $totalSize

$row++
$sheet.Cells.Item($row, 2) = "Tổng dung lượng thư mục:"
$row++
foreach ($entry in $directorySizes.GetEnumerator()) {
    $sheet.Cells.Item($row, 1) = $entry.Key
    $sheet.Cells.Item($row, 3) = $entry.Value
    $row++
}

$savePath = "C:\Result.xlsx"
$workbook.SaveAs($savePath)
$excel.Quit()

[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
