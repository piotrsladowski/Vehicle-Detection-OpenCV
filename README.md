# IO_VehicleDetection

Install all required modules using `pip install -r requirements.txt`
## Virtualenv 
1. Get `virtualenv` using `pip install virtualenv`
2. `virtualenv --python C:\Path\To\Python\python.exe env`. Get Python 3.8.6
3. `cd <project-directory>`
4. `./env/Scripts/activate`
5. Run app by typing `python ./src/main.py`

__Here you go__ -> make sure to always run `venv` when doing the project</br>
*Hint:* Set the Python interpreter in VSCode or PyCharm

## Pipenv - Python packaging tool
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

## [yolov4.weights](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights) - Download and place in the "model" directory


## [Install K-Lite Codec Pack](https://files3.codecguide.com/K-Lite_Codec_Pack_1590_Standard.exe)
