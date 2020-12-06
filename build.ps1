#######################################
# Test build setup for Vehicle_Detector with _pyinstaller_
#
# Copyright 2020 by Smendwoski Mateusz, Sladowski Piotr, Twardosz Adam
#######################################


# At first ask for admin permissions
$vlcInstalled = 0
$vlcPath = ''

$vlcLine = (Get-WMIObject -Query "SELECT * FROM Win32_Product Where Name Like '%VLC media player%'") | Select Caption,InstallLocation 
if ($vlcLine.Length -gt 0) {
    $vlcInstalled = 1
    $vlcPath = $vlcLine.InstallLocation
}



# Find local dll's


# Then download necessary files
# YOLO MODELS' yolovX.weights

# libvlc.dll download (if not found on system hard drive)

# _pyinstaller_ section


# ending setup