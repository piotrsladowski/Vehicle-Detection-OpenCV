import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
from imutils.video import FPS
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

    def __init__(self, progressBar, sourceVideoPath):
        super().__init__()
        self.confThreshold = 0.85  
        self.nmsThreshold = 0.4    
        self.inpWidth = 320        
        self.inpHeight = 320       
        self.progressBar = progressBar
        self.sourceVideoPath = sourceVideoPath
        self.statistics = {
            "total_vehicles": 0,
            "light_vehicles": 0,
            "heavy_vehicles": 0,
            "two_wheel_vehicles": 0,
            "unknown_vehicles": 0
        }
        self.logList = ["test", "okej"]
        self.classesInterested = ['bicycle', 'motorbike', 'car', 'bus', 'truck']
        self.logger = logging.getLogger(name='Processor')
        

    def run(self):
        if not os.path.isfile(self.sourceVideoPath):
            return None

        classesName, modelConfiguration, modelWeights, *_ = ALLOWED_PATHS.values()
        classes = self.load_classes(classesName)

        net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        cap = self.get_video_capture(self.sourceVideoPath)
        self.progressBar.setMaximum(int(cap.get(cv.CAP_PROP_FRAME_COUNT)))
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
       
        # USAGE EXAMPLE
        self.logger.debug("VEHICLE DETECTED".format())

        try:
            if self.process_capture(cap, classes, net, vid_writer) == 0:
                self.logger.handlers.clear()
                self.on_data_finish.emit({"done": True, "outVideo": outputVideoFile, "outLog": outputLogFile, "stats": self.statistics})
        except Exception as e:
            self.logger.error(str(e))
            self.logger.handlers.clear()
            self.on_data_finish.emit({"done": False, "outVideo": None, "outLog": None, "stats": None})

    def load_classes(self, path):
        if path.lower().endswith('.names') and path in ALLOWED_PATHS.values():
            with open(path, 'rt') as f:
                return f.read().rstrip('\n').split('\n')
        return None

    def get_outputs_names(self, network):
        layersNames = network.getLayerNames()
        return [layersNames[i[0] - 1] for i in network.getUnconnectedOutLayers()]

    def draw_pred(self, frame, classes, classId, conf, left, top, right, bottom):
        if classes[classId] not in self.classesInterested:
            return None

        cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

        label = '%.2f' % conf

        if classes:
            # print(f"classID: {classId}") -> Statystyki
            label = '%s:%s' % (classes[classId], label) if classes[classId] in self.classesInterested else None

        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

    def post_process(self, frame, classes, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            self.draw_pred(frame, classes, classIds[i], confidences[i], left, top, left + width, top + height)

    def get_video_capture(self, path):
        if not os.path.isfile(path):
            sys.exit(1)
        else:
            return cv.VideoCapture(path)

    def process_capture(self, cap, classes, net, vid_writer):
        exit_status = 1
        fps = FPS().start()
        while True:

            _, frame = cap.read()
            self.progressBar.setValue(int(cap.get(cv.CAP_PROP_POS_FRAMES)))

            frame = imutils.resize(frame)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])
           
            # Processing has beed properly ended
            if int(cap.get(cv.CAP_PROP_POS_FRAMES)) == int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
                exit_status = 0
                break

            blob = cv.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False) 

            net.setInput(blob)

            outs = net.forward(self.get_outputs_names(net))

            self.post_process(frame, classes, outs)

            vid_writer.write(frame.astype(np.uint8))
            fps.update()
            
        fps.stop()
        cap.release()
        cv.destroyAllWindows()
        return exit_status
