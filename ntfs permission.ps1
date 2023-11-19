# Define the root directory you want to perform the operation on
$rootPath = "D:\BackupFILE"

# Define a function to update permissions
Function Set-Permissions ($path) {
    # Check if the path exists
    if (Test-Path $path) {
        # Remove inherited permissions
        $acl = Get-Acl -Path $path
        $acl.SetAccessRuleProtection($true, $false)
        Set-Acl -Path $path -AclObject $acl

        # Remove read-only attribute
        Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
            $_.Attributes = $_.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
        }

        # Set permissions for everyone and administrators
        $acl = Get-Acl -Path $path
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("everyone","FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
        $acl.AddAccessRule($rule)

        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("BUILTIN\Administrators","FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
        $acl.AddAccessRule($rule)

        # Write the ACL back to the directory
        Set-Acl -Path $path -AclObject $acl
    }
    else {
        Write-Host "Path '$path' does not exist."
    }
}

# Perform the operation on each directory and file
Get-ChildItem -Path $rootPath -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    Set-Permissions $_.FullName
}
