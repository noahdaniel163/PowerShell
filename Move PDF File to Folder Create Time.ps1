# Specify the IP address and path of the scan directory
$scanPath = '\\192.168.0.152\scan\deposit'

# Get a list of PDF files in the directory
$pdfFiles = Get-ChildItem -Path $scanPath -Filter *.pdf

foreach ($file in $pdfFiles) {
    # Get information about the file creation time
    $creationDate = $file.CreationTime
    $year = $creationDate.Year
    $month = $creationDate.Month.ToString("00") # Format the month to have two digits (01 for January)

    # Format the destination folder name
    $destinationFolder = Join-Path $scanPath -ChildPath "$year-$month"

    # Check if the folder already exists
    if (-not (Test-Path $destinationFolder)) {
        New-Item -ItemType Directory -Path $destinationFolder
    }

    # Move the PDF file to the new folder
    Move-Item -Path $file.FullName -Destination $destinationFolder
}

Write-Host "Creating folders and moving PDF files completed."
