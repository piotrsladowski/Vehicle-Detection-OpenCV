# IO_VehicleDetection

Project developed under Python 3.8.6
## Virtualenv 
1. Get `virtualenv` using `pip3 install virtualenv`
2. `virtualenv <envName>`. 
3. `cd <project-directory>`
4. `./<envName>/Scripts/activate`
5. Install all required modules using `pip3 install -r requirements.txt`
6. Run app by typing `python ./src/main.py`

__Here you go__ -> make sure to always run `venv` when doing the project</br>
*Hint:* Set the Python interpreter in VSCode or PyCharm

---

## Pipenv - Python packaging tool - an alternative to virtualenv 
1. Activate Pipenv environment: `pipenv shell`
2. Install packages: `pipenv install`
3. Run app by typing `python ./src/main.py`

## Tensorflow - check if properly installed
```python
python -c 'import tensorflow as tf; print(tf.__version__)'
```

## [ADDITION*] tensorflow-gpu setup
1. Install `tensorflow` version `2.3.1`
2. Uninstall current version of  `numpy`
3. Install `numpy` versoin `1.18.5`
4. Check your graphics driver is up to date. 
5. Install `tensorflow gpu` version `*`
6. Install [`CUDA Toolkit 10.1 update2`](https://developer.nvidia.com/cuda-10.1-download-archive-update2?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal)
7. Run using cmd: 
```shell
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\extras\CUPTI\lib64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\include;%PATH%
SET PATH=C:\tools\cuda\bin;%PATH%
```
8. PC restart may be necessary to apply changes.

---

## Weights - download and place in the "model" directory
### [YOLOv4](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights)

### [YOLOv3-tiny](https://pjreddie.com/media/files/yolov3-tiny.weights)

### [YOLOv3](https://pjreddie.com/media/files/yolov3.weights)

---

### Make sure to download libvlc.dll and put it into dlls directory in project directory (in order video player to work)