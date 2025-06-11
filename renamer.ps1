#
# For reference in the script I am calling:
#     data the top level folder
#     case the child folders
#     files, the children of the case folders
#
# Lines to edit:
#   10 - Path to 'data' folder
#
#
# Questions:
#   - What if a file already has a <index-like> start? (line 31)

$dataFolder = "C:\path\to\data" # Modify this path to your data folder location

function Process-CaseFolder {
    param (
        [string]$casePath
    )

    Write-Host "Processing folder: $casePath"

    # Get all files in the folder
    $allChildFiles = Get-ChildItem -Path $casePath -File

    # Separate already prefixed files from unprefixed files
    $prefixedFiles = @()
    $unprefixedFiles = @()

    foreach ($file in $allChildFiles) {
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
        $newPath = Join-Path -Path $casePath -ChildPath $newName

        Write-Host "Renaming $($file.FullName) to $newPath"

        try {
            Rename-Item -Path $file.FullName -NewName $newName -ErrorAction Stop
            $nextPrefix++
        } catch {
            Write-Error "Failed to rename $($file.FullName): $_"
        }
    }
}

# End of Process-CaseFolder function

# Get all case folders
$caseFolders = Get-ChildItem -Path $dataFolder -Directory

# Process each case folder
foreach ($folder in $caseFolders) {
    Process-CaseFolder -folderPath $folder.FullName
}

Write-Host "File indexing completed."
