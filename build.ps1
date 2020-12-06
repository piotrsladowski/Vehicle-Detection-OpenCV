#######################################
# Test build setup for Vehicle_Detector with _pyinstaller_
#
# Copyright 2020 by Smendwoski Mateusz, Sladowski Piotr, Twardosz Adam
#######################################

# Storing caller working directory
$uwd = $PWD
# Setting script working directory
Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

# At first ask for admin permissions
# ~actually not yet needed

# Find local dll's
$vlcInstalled = 0
$vlcLine = Get-ChildItem -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\ | Get-ItemProperty | Select-Object DisplayName, InstallLocation | Where-Object {$_.DisplayName -like "VLC media player"} 
if ($vlcLine.Length -gt 0) {
    $vlcInstalled = 1
    $libvlcPath = $vlcLine.InstallLocation + "\libvlc.dll"
    Copy-Item $libvlcPath -Destination "./dlls/libvlc.dll"
}

# Then download necessary files
# YOLO MODELS' yolovX.weights
(New-Object System.Net.WebClient).DownloadFile("https://pjreddie.com/media/files/yolov3.weights", "./src/model/yolov3.weights")
(New-Object System.Net.WebClient).DownloadFile("https://pjreddie.com/media/files/yolov3-tiny.weights", "./src/model/yolov3-tiny.weights")
(New-Object System.Net.WebClient).DownloadFile("https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights", "./src/model/yolov4.weights")

# libvlc.dll download (if not found on system hard drive)
if $vlcInstalled == 0 {
    (New-Object System.Net.WebClient).DownloadFile("https://downloads.dllspedia.com/dlls/libvlc_dll_64bit_2_2_2_0.zip", "./dlls/libvlc.zip")
    Expand-Archive "./dlls/libvlc.zip" -DestinationPath "./dlls/"
    Remove-Item "./dlls/libvlc.zip"
}

# _pyinstaller_ section
./env/Scripts/activate
pip install -r ./requirements.txt

# end setup