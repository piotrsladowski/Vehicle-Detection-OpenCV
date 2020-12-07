# Vehicle Detection
1. [ Description. ](#desc)
2. [ Features ](#features)
3. [ Technologies used ](#techno)
4. [ Installation ](#install)
5. [ Screen shots ](#screens)
6. [ License ](#license)


<a name="desc"></a>
## 1. Description
A cross-platform application made as part of the project from software engineering on AGH University of Science and Technology.

<a name="features"></a>
## 2. Features and functionality
+ Detection
+ Categorization
+ Possibility to run on different models
+ Frame skipping & interpolation


<a name="techno"></a>
## 3. Technologies used
* [Python Language](https://www.python.org) - application logic
* [OpenCV](https://opencv.org) - object detecion framwork
* [PyQt](https://wiki.python.org/moin/PyQt) - user inteface framework
* [FFmpeg](https://ffmpeg.org) - video processing

<a name="install"></a>
## 3. Installation
PowerShell is highly recommended. **No other legacy environments are supported** Linuks is also not supported.<br>
Project developed under Python 3.8.6

### For dummies
Just run *build.ps1*

### For geeks
### Virtualenv 
1. Get `virtualenv` using `pip3 install virtualenv`
2. `cd <project-directory>`
3. `virtualenv <envName>` 
4. `.\<envName>\Scripts\activate`
5. Install all required modules using `pip3 install -r requirements.txt`
6. Run app by typing `python .\src\main.py`

__Here you go__ -> make sure to always run `venv` when doing the project</br>
*Hint:* Set the Python interpreter in VSCode or PyCharm

---

### Pipenv - Python packaging tool - an alternative to virtualenv 
1. Activate Pipenv environment: `pipenv shell`
2. Install packages: `pipenv install`
3. Run app by typing `python ./src/main.py`

---

### Weights - download and place in the "model" directory
#### [YOLOv4](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights)

#### [YOLOv3-tiny](https://pjreddie.com/media/files/yolov3-tiny.weights)

#### [YOLOv3](https://pjreddie.com/media/files/yolov3.weights)

---
### Configure libVLC and FFmpeg

libVLC is required for internal video player.
FFmpeg is required for interpolating video.
1. Download latest VLC [3.0.11](https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe).
2. Extract *libvlc.dll* and copy it into the *dlls* folder.
3. Install FFmpeg `choco install ffmpeg`<br>
3.1 Alternatively download latest build from [here](https://www.gyan.dev/ffmpeg/builds/) and add ffmpeg.exe to the `$Path` <br> `$env:Path += ";<path_to_ffmpeg>"`.

<a name="screens"></a>
## 4. Screen shots
![Start Screen](https://github.com/piotrsladowski/IO_VehicleDetection/blob/main/screens/tab_start.png)
![Start Screen - ComboBox](https://github.com/piotrsladowski/IO_VehicleDetection/blob/main/screens/tab_combo.png)
![Start Screen after processing](https://github.com/piotrsladowski/IO_VehicleDetection/blob/main/screens/tab_main.png)
![Video tab](https://github.com/piotrsladowski/IO_VehicleDetection/blob/main/screens/tab_video.png)
![Logs tab](https://github.com/piotrsladowski/IO_VehicleDetection/blob/main/screens/tab_logs.png)
![Stats tab](https://github.com/piotrsladowski/IO_VehicleDetection/blob/main/screens/tab_stats.png)

<a name="crea"></a>
## 5. Creators
Smendowski Mateusz, Śladowski Piotr, Twardosz Adam

<a name="license"></a>
## 6. License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
