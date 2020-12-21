#######################################
# Test build setup for Vehicle_Detector with _pyinstaller_
#
# Copyright 2020 by Smendwoski Mateusz, Sladowski Piotr, Twardosz Adam
#######################################

# Storing caller working directory
$uwd = $PWD
# Setting script working directory
Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

# Find local dll's
$vlcInstalled = 0
$vlcLine = Get-ChildItem -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\ | Get-ItemProperty | Select-Object DisplayName, InstallLocation | Where-Object {$_.DisplayName -like "VLC media player"} 
if ($vlcLine.Length -gt 0) {
    $vlcInstalled = 1
    $libvlcPath = $vlcLine.InstallLocation + "\libvlc.dll"
    Copy-Item $libvlcPath -Destination "./dlls/libvlc.dll"
}

$ffmpeg = 0
$ffmpegLine = $env:Path.Split(';') | Select-String -pattern 'ffmpeg'
if ($ffmpegLine.Length -gt 0) {
    $ffmpeg = 1
    Write-Host "ffmpeg already installed"
} elseif ((choco --version).Length -gt 0) {
    if ((choco list --local | Select-String -pattern "ffmpeg").Length -gt 0) {
        $ffmpeg = 1
        Write-Host "ffmpeg already installed with chocolatey"
    }
} elseif ((scoop).Length -eq 30) {
    if ((scoop list | Select-String -pattern "ffmpeg").Length -gt 0) {
        $ffmpeg = 1
        Write-Host "ffmpeg already installed with scoop"
    }
}

# Then download necessary files
# YOLO MODELS' yolovX.weights
if (!(Test-Path -Path "./src/model/yolov3.weights")) {
    Invoke-WebRequest -Uri "https://pjreddie.com/media/files/yolov3.weights" -OutFile "./src/model/yolov3.weights"
}
if (!(Test-Path -Path "./src/model/yolov3-tiny.weights")) {
    Invoke-WebRequest -Uri "https://pjreddie.com/media/files/yolov3-tiny.weights" -OutFile "./src/model/yolov3-tiny.weights"
}
if (!(Test-Path -Path "./src/model/yolov4.weights")) {
    Invoke-WebRequest -Uri "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights" -Outfile "./src/model/yolov4.weights"
}
# libvlc.dll download (if not found on system hard drive)
if ($vlcInstalled -eq 0) {
    Invoke-WebRequest -Uri "https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBcnVsR3pSOEsyS0NoTUJjRUw3VEJ4OHR0eWlEMFE_ZT02TUVPR0I/root/content" -OutFile "./dlls/libvlc.dll"
}

if ($ffmpeg -eq 0) {
    Invoke-WebRequest -Uri "https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2020-12-07-12-50/ffmpeg-N-100214-g95fd790c14-win64-gpl-vulkan.zip" -OutFile "./ffmpeg.zip"
    Expand-Archive "./ffmpeg.zip" -DestinationPath "./ffmpeg/"
    Copy-Item "./ffmpeg/ffmpeg-N-100214-g95fd790c14-win64-gpl-vulkan/bin/ffmpeg.exe" -Destination "./"
    Remove-Item -Recurse "./ffmpeg"
    Remove-Item "./ffmpeg.zip"
}

# venv section
pip3 install virtualenv
virtualenv env
./env/Scripts/activate
pip3 install -r ./requirements.txt

# end setup