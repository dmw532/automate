# Script to rename files in case folders based on creation date
$dataFolder = "C:\path\to\data" # Modify this path to your data folder location

# Function to process a case folder
function Process-CaseFolder {
    param (
        [string]$folderPath
    )

    Write-Host "Processing folder: $folderPath"

    # Get all files in the folder
    $allFiles = Get-ChildItem -Path $folderPath -File

    # Separate already prefixed files from unprefixed files
    $prefixedFiles = @()
    $unprefixedFiles = @()

    foreach ($file in $allFiles) {
        if ($file.Name -match '^\d+\-') {
            $prefixedFiles += $file
        } else {
            $unprefixedFiles += $file
        }
    }

    # Find the highest prefix number used
    $nextPrefix = 1
    if ($prefixedFiles.Count -gt 0) {
        $highestPrefix = 0
        foreach ($file in $prefixedFiles) {
            if ($file.Name -match '^(\d+)\-') {
                $prefixNum = [int]$Matches[1]
                if ($prefixNum -gt $highestPrefix) {
                    $highestPrefix = $prefixNum
                }
            }
        }
        $nextPrefix = $highestPrefix + 1
    }

    # Sort unprefixed files by creation date
    $sortedFiles = $unprefixedFiles | Sort-Object CreationTime

    # Rename files with appropriate prefix
    foreach ($file in $sortedFiles) {
        $newName = "$nextPrefix-$($file.Name)"
        $newPath = Join-Path -Path $folderPath -ChildPath $newName

        Write-Host "Renaming $($file.FullName) to $newPath"

        try {
            Rename-Item -Path $file.FullName -NewName $newName -ErrorAction Stop
            $nextPrefix++
        } catch {
            Write-Error "Failed to rename $($file.FullName): $_"
        }
    }
}

# Get all case folders
$caseFolders = Get-ChildItem -Path $dataFolder -Directory

# Process each case folder
foreach ($folder in $caseFolders) {
    Process-CaseFolder -folderPath $folder.FullName
}

Write-Host "File renaming completed."
