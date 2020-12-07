import cv2 as cv
import sys
from datetime import datetime as dt
import time
import math
import asyncio
import queue
import os.path
import numpy as np
import imutils
from PySide2 import QtCore
from PySide2.QtCore import QThread, Signal
import ffmpeg
import logging

M0 = {
    "classesPath": "src/model/classes.names",
    "modelConfigurationPath": "src/model/yolov3-tiny.cfg",
    "modelWeightsPath": "src/model/yolov3-tiny.weights",
}

M1 = {
    "classesPath": "src/model/classes.names",
    "modelConfigurationPath": "src/model/yolov3-320.cfg",
    "modelWeightsPath": "src/model/yolov3.weights",
}

M2 = {
    "classesPath": "src/model/classes.names",
    "modelConfigurationPath": "src/model/yolov4.cfg",
    "modelWeightsPath": "src/model/yolov4.weights",
}

M3 = {
    "classesPath": "src/model/classes.names",
    "modelConfigurationPath": "src/model/yolov3-608.cfg",
    "modelWeightsPath": "src/model/yolov3.weights",
}

def printf(format, *args):
    sys.stdout.write(format % args)

class QueuingHandler(logging.Handler):
    def __init__(self, *args, message_queue, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.message_queue = message_queue

    def emit(self, record):
        self.message_queue.put(self.format(record).rstrip('\n'))

class VideoProcessor(QThread):

    on_data_finish = Signal(dict)
    on_progress = Signal(float)

    def __init__(self, sourceVideoPath, model):
        super().__init__()

        # Windows size in YOLO. Available options are: 320, 416, 608.
        # This field must be the same as in the YOLO*.cfg file.
        self.inpWidth = 416        
        self.inpHeight = 416  
        if model == 0:
            self.model = M0
            self.inpWidth = 416        
            self.inpHeight = 416
            print("Chosen model: {}".format("YOLOv3-tiny"))
        elif model == 1:
            self.model = M1
            self.inpWidth = 320        
            self.inpHeight = 320
            print("Chosen model: {}".format("YOLOv3-320"))
        elif model == 2:
            self.model = M2
            self.inpWidth = 416        
            self.inpHeight = 416
            print("Chosen model: {}".format("YOLOv4 <Default>"))
        elif model == 3:
            self.model = M3
            self.inpWidth = 608        
            self.inpHeight = 608
            print("Chosen model: {}".format("YOLOv3-608"))
        else:
            print("Wrong model. Can't find it!")

        self.confThreshold = 0.50   # Only objects with greater confidence will be detecting
        self.nmsThreshold = 0.7 
        self.sourceVideoPath = sourceVideoPath
        # How many frames will be skipped. 
        # E.g if value 3 is selected then only 1 frame per 3 frames will be analyzed.
        # 1 is a default value, no frames will be skipped.
        self.frameSkipRate = 0
        self.detectionsCache = []
        self.statistics = {
            "total_vehicles": 0,
            "light_vehicles": 0,
            "heavy_vehicles": 0,
            "two_wheel_vehicles": 0,
            "unknown_vehicles": 0
        }
        self.classesInterested = ['bicycle', 'motorbike', 'car', 'bus', 'truck']
        self.logger = logging.getLogger(name='Vehicle Detector')
        

    def run(self):
        if not os.path.isfile(self.sourceVideoPath):
            return None

        classesName, modelConfiguration, modelWeights, *_ = self.model.values()
        classes = self.load_classes(classesName)

        net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        cap = self.get_video_capture(self.sourceVideoPath)
        self.fps = int(cap.get(cv.CAP_PROP_FPS))
        if self.fps < 10 and self.fps % 2:
            self.frameSkipRate = 2
        elif self.fps < 10 and not self.fps % 2:
            self.frameSkipRate = 1
        elif self.fps > 10 and self.fps in [15,20,25,30,60]:
            self.frameSkipRate = 5
        else:
            self.frameSkipRate = 1
        self.current_frame = 0
        self.maximum = cap.get(cv.CAP_PROP_FRAME_COUNT)
        currFilename, currExtenstion = self.sourceVideoPath.split('.')
        writerVideoFile = f"{currFilename}_middle.{currExtenstion}"
        outputVideoFile = f"{currFilename}_rendered.{currExtenstion}"

        logFormat = '%(asctime)s: %(name)8s: %(levelname)8s: %(message)s'
        outputLogFile = f"{currFilename}_rendered.log"
        logging.basicConfig(filename=outputLogFile, filemode='w',
                            format=logFormat, level=logging.DEBUG)
    

        message_queue = queue.Queue()
        handler = QueuingHandler(message_queue=message_queue, level=logging.DEBUG)

        formatter = logging.Formatter(logFormat)
        formatter.default_time_format = f"{dt.hour}:{dt.minute}:{dt.second}"
        handler.setFormatter(formatter)                       
        
        vid_writer = cv.VideoWriter(writerVideoFile,
                    cv.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv.CAP_PROP_FPS) / self.frameSkipRate),
                    (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))) 
       
        loop = asyncio.new_event_loop()
        try:
            if self.process_capture(cap, classes, net, vid_writer) == 0:
                self.logger.handlers.clear()
                vid_writer.release()
                interpolate = loop.create_task(self.interp_basic(writerVideoFile, outputVideoFile, self.fps))
                loop.run_until_complete(interpolate)
                loop.close()
                self.on_progress.emit(self.current_frame / self.maximum)
                self.on_data_finish.emit({"done": True, "outVideo": outputVideoFile, "outLog": outputLogFile, "stats": self.statistics})
        except Exception as e:
            self.logger.error(str(e))
            self.logger.handlers.clear()
            self.on_data_finish.emit({"done": False, "outVideo": None, "outLog": None, "stats": None})

    def load_classes(self, path):
        # Load from coco.names classes specified in __init__
        if path.lower().endswith('.names') and path in self.model.values():
            with open(path, 'rt') as f:
                return f.read().rstrip('\n').split('\n')
        print("No classes loaded")
        return None

    def get_outputs_names(self, network):
        layersNames = network.getLayerNames()
        return [layersNames[i[0] - 1] for i in network.getUnconnectedOutLayers()]
    
    async def interp_basic(self, iVideo, oVideo, fps):
        input = ffmpeg.input(iVideo)
        video_interp = input.video.filter('minterpolate', fps)
        output = ffmpeg.output(video_interp, oVideo)
        ffmpeg.run(output)

    def log_object(self, classes, class_id, confidence):
        if classes[class_id] in self.classesInterested:
            if classes[class_id] == "car":
                self.statistics["light_vehicles"] += 1
            elif classes[class_id] == "bus" or classes[class_id] == "truck":
                self.statistics["heavy_vehicles"] += 1
            elif classes[class_id] == "bicycle" or classes[class_id] == "motorbike":
                self.statistics["two_wheel_vehicles"] += 1
            self.statistics["total_vehicles"] += 1
            self.logger.info(f"New class: {classes[class_id]} detected in {self.current_frame/self.fps} second with conf: {confidence}")

    def draw_pred(self, frame, classes, classId, conf, leftBtmX, leftBtmY, rightTopX, rightTopY):
        if classes[classId] not in self.classesInterested:
            return None

        # Draw a rectangle with lightblue line borders of thickness of 3 px
        cv.rectangle(frame, (leftBtmX, leftBtmY), (rightTopX, rightTopY), (255, 178, 50), 3)

        label = '%.2f' % conf

        if classes:
            label = '%s:%s' % (classes[classId], label) if classes[classId] in self.classesInterested else None
        
        confidence = label.split(':')[1]
        self.log_object(classes, classId, confidence)

        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        leftBtmY = max(leftBtmY, labelSize[1])
        # Draw a white label background
        cv.rectangle(frame, (leftBtmX, leftBtmY - round(1.5*labelSize[1])), (leftBtmX + round(1.5*labelSize[0]), leftBtmY + baseLine), (255, 255, 255), cv.FILLED)
        # Draw a black text label of a detected vehicle
        cv.putText(frame, label, (leftBtmX, leftBtmY), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

    def post_process(self, frame, classes, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = [] 

        # Parse coordinates of detected objects to rectangles indices.
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    # OpenCV returns relative indices of detected objects
                    # e.g if your frame is 1920px wide and center of the object is on 768px
                    # then OpenCV will return 0.4.
                    # Because every rectangle can be defined by two points on the surface
                    # we will obtain left bottom and width and height of a rectangle.
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    leftBtmX = int(center_x - width / 2)
                    leftBtmY = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([leftBtmX, leftBtmY, width, height])
                else:
                    self.statistics["unknown_vehicles"] += 1

        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            leftBtmX = box[0]
            leftBtmY = box[1]
            width = box[2]
            height = box[3]
            # Draw rectangles on the frame
            self.draw_pred(frame, classes, classIds[i], confidences[i], leftBtmX, leftBtmY, leftBtmX + width, leftBtmY + height)

        # return frame

    def get_video_capture(self, path):
        if not os.path.isfile(path):
            print("Input file not found")
            sys.exit(1)
        else:
            return cv.VideoCapture(path)

    def process_capture(self, cap, classes, net, vid_writer):
        exit_status = 1
        start = time.time()
        while True:
            _, frame = cap.read()
            self.current_frame = cap.get(cv.CAP_PROP_POS_FRAMES)
            self.on_progress.emit(self.current_frame / self.maximum)
            frame = imutils.resize(frame)
            # Process frames in a grayscale. 
            # Comment next 2 lines if you want to have a RGB colors
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])
           
            # Processing has beed properly ended
            if int(cap.get(cv.CAP_PROP_POS_FRAMES)) == int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
                exit_status = 0
                break

            if self.current_frame % self.frameSkipRate:
                # vid_writer.write(frame.astype(np.uint8))
                continue
            blob = cv.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False) 
            net.setInput(blob)
            outs = net.forward(self.get_outputs_names(net))
            self.post_process(frame, classes, outs)
            vid_writer.write(frame.astype(np.uint8))

        end = time.time()
        printf("Video Processing done in %.2f seconds.\n", (end-start))
        print(f"Total number of processed frames: {self.maximum}")
        printf("Mean frames per second rate: %.2f\n", cap.get(cv.CAP_PROP_FRAME_COUNT)/(end-start))
        cap.release()
        cv.destroyAllWindows()
        return exit_status
