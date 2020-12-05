import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
import imutils
from PySide2 import QtCore
from PySide2.QtCore import QThread, Signal
import logging
import queue
from datetime import datetime as dt


ALLOWED_PATHS = {
    "classesPath": "src/model/classes.names",
    "modelConfigurationPath": "src/model/yolov4.cfg",
    "modelWeightsPath": "src/model/yolov4.weights",
}

class QueuingHandler(logging.Handler):
    def __init__(self, *args, message_queue, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.message_queue = message_queue

    def emit(self, record):
        self.message_queue.put(self.format(record).rstrip('\n'))

class VideoProcessor(QThread):

    on_data_finish = Signal(dict)
    on_progress = Signal(float)

    def __init__(self, sourceVideoPath):
        super().__init__()
        self.confThreshold = 0.85   # Only objects with greater confidence will be detecting
        self.nmsThreshold = 0.4
        # Windows size in YOLO. Available options are: 320, 416, 608.
        # Remeber to update width and height fields in yolov4.cfg    
        self.inpWidth = 608        
        self.inpHeight = 608
        self.sourceVideoPath = sourceVideoPath
        # How many frames will be skipped. 
        # E.g if value 3 is selected then only 1 frame per 3 frames will be analyzed.
        # 1 is a default value, no frames will be skipped.
        self.frameSkipperCount = 1
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

        classesName, modelConfiguration, modelWeights, *_ = ALLOWED_PATHS.values()
        classes = self.load_classes(classesName)

        net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        cap = self.get_video_capture(self.sourceVideoPath)
        self.fps = int(cap.get(cv.CAP_PROP_FPS))
        self.current_frame = 0
        self.maximum = cap.get(cv.CAP_PROP_FRAME_COUNT)
        currFilename, currExtenstion = self.sourceVideoPath.split('.')
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
        
        self.logger.addHandler(handler)

        vid_writer = cv.VideoWriter(outputVideoFile,
                    cv.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv.CAP_PROP_FPS)),
                    (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))) 
       
        try:
            if self.process_capture(cap, classes, net, vid_writer) == 0:
                self.logger.handlers.clear()
                self.on_progress.emit(self.current_frame / self.maximum)
                self.on_data_finish.emit({"done": True, "outVideo": outputVideoFile, "outLog": outputLogFile, "stats": self.statistics})
        except Exception as e:
            self.logger.error(str(e))
            self.logger.handlers.clear()
            self.on_data_finish.emit({"done": False, "outVideo": None, "outLog": None, "stats": None})

    def load_classes(self, path):
        # Load from coco.names classes specified in __init__
        if path.lower().endswith('.names') and path in ALLOWED_PATHS.values():
            with open(path, 'rt') as f:
                return f.read().rstrip('\n').split('\n')
        print("No classes loaded")
        return None

    def get_outputs_names(self, network):
        layersNames = network.getLayerNames()
        return [layersNames[i[0] - 1] for i in network.getUnconnectedOutLayers()]
    
    def compare_pred(self, tempDetections):
        if len(self.detectionsCache) == 0:
            return [row[0] for row in tempDetections]
        sanitizedDetections = []
        # Compare all points in peer-to-peer scenario
        tempParameters, cachedParameters = [], []
        for pred in tempDetections:
            # Struktura pred w obiegu: [[705, 21, 193, 109], [0.41815326, 0.071146525]]
            tempParameters = pred[0]
            print(f"Pred - wartości bezwzgędne: {tempParameters}")
            for cachePred in self.detectionsCache:
                cachedParameters = cachePred[0]
                print(f"Cached pred - wartości bezwzględne: {cachedParameters}")
                # Compare distance by simple Pitagoras
                #print(f"X1 {X1}, Y1 {Y1}, X2 {X2}, Y2 {Y2}")
                X1 = tempParameters[0]
                Y1 = tempParameters[1]
                X2 = cachedParameters[0]
                Y2 = cachedParameters[1]
                if ((X2-X1)**2 + (Y2-Y1)**2)**0.5 < 0.6:
                    sanitizedDetections.append(cachedParameters)
                else:
                    sanitizedDetections.append(tempParameters)
        return sanitizedDetections

    def draw_pred(self, frame, classes, classId, conf, leftBtmX, leftBtmY, rightTopX, rightTopY):
        # Draw a rectangle with lightblue line borders of thickness of 3 px
        cv.rectangle(frame, (leftBtmX, leftBtmY), (rightTopX, rightTopY), (255, 178, 50), 3)

        label = '%.2f' % conf
        if classes:
            label = '%s:%s' % (classes[classId], label) if classes[classId] in self.classesInterested else None
        
        if (label == None):
            return None
        # Update number of detected vehicles
        if classes[classId] == "car":
            self.statistics["light_vehicles"] += 1
        elif classes[classId] == "bus" or classes[classId] == "truck":
            self.statistics["heavy_vehicles"] += 1
        elif classes[classId] == "bicycle" or classes[classId] == "motorbike":
            self.statistics["two_wheel_vehicles"] += 1
        else:
            self.statistics["unknown_vehicles"] += 1
        self.statistics["total_vehicles"] += 1
        self.logger.info(f"New class: {classes[classId]} detected in {self.current_frame/self.fps} second with conf: {label.split(':')[1]}")

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
        doubledDetections = [] # Store all 

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
                    if classes[classId] in self.classesInterested:
                        classIds.append(classId)
                    else:
                        continue
                    confidences.append(float(confidence))
                    boxes.append([leftBtmX, leftBtmY, width, height])
                    print("X: {0}".format(detection[0]))
                    print("Y: {0}".format(detection[1]))
                    doubledDetections.append([[leftBtmX, leftBtmY, width, height], [detection[0], detection[1]]])
                    print("Bezwzględne: {0}".format([leftBtmX, leftBtmY, width, height]))
                    # X: 0.5671080946922302
                    # Y: 0.14301526546478271
                    # Bezwzględne: [970, 103, 235, 101]

        boxes = self.compare_pred(doubledDetections)
        # print(boxes)
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
        # UNCOMMENT TO USE compare_pred:
        self.detectionsCache.clear()
        self.detectionsCache = doubledDetections

    def get_video_capture(self, path):
        if not os.path.isfile(path):
            print("Input file not found")
            sys.exit(1)
        else:
            return cv.VideoCapture(path)

    def process_capture(self, cap, classes, net, vid_writer):
        exit_status = 1
        while True:
            _, frame = cap.read()
            
            self.current_frame = cap.get(cv.CAP_PROP_POS_FRAMES)
            self.on_progress.emit(self.current_frame / self.maximum)
            frame = imutils.resize(frame)
            # Process frames in a grayscale. 
            # Comment next 2 lines if you want to have a RGB colors
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])
           
            # Speed up algorithm by skipping frames
            if(self.frameSkipperCount != 1 and (self.current_frame % self.frameSkipperCount == 0)):
                vid_writer.write(frame.astype(np.uint8))
                continue
            # Processing has beed properly ended
            if int(cap.get(cv.CAP_PROP_POS_FRAMES)) == int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
                exit_status = 0
                break

            blob = cv.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False) 

            net.setInput(blob)

            outs = net.forward(self.get_outputs_names(net))

            self.post_process(frame, classes, outs)

            vid_writer.write(frame.astype(np.uint8))

        # Close input video file    
        cap.release()
        cv.destroyAllWindows()
        return exit_status
