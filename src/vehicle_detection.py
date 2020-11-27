import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
from imutils.video import FPS
import imutils


# INITAL PARAMETERS
confThreshold = 0.85  #Confidence threshold
nmsThreshold = 0.4    #Non-maximum suppression threshold
inpWidth = 320        #Width of network's input image
inpHeight = 320       #Height of network's input image

ALLOWED_PATHS = {
    "classesPath": "model/classes.names",
    "modelConfigurationPath": "model/yolov4.cfg",
    "modelWeightsPath": "model/yolov4.weights",
}

CLASSES_INTERESTED = ['bicycle', 'motorbike', 'car', 'bus', 'truck']

VERSION = 'v1.1'

def main(sourceVideoPath):
    # TODO: Sprawdzić czy sourceVideoPath istnieje
    classesName, modelConfiguration, modelWeights, *_ = ALLOWED_PATHS.values()
    classes = loadClasses(classesName)

    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    windowName = f"Vehicle Detector {VERSION}"
    cv.namedWindow(windowName, cv.WINDOW_NORMAL)
 
    cap = getVideoCapture(sourceVideoPath)
    TOTAL_FRAMES_NUM = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    currFilename, currExtenstion = sourceVideoPath.split('.')     
    outputFile = f"{currFilename}_rendered.{currExtenstion}"

    # TODO: Sprawdzić czy istnieje taki plik outputFile, jeśli tak to usunąć

    vid_writer = cv.VideoWriter(outputFile,
                cv.VideoWriter_fourcc('M','J','P','G'), 30,
                (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                round(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))) 

    processCapture(cap, classes, net, vid_writer)

    cap.release()
    cv.destroyAllWindows()

    return 
    

def loadClasses(path):
    if path.lower().endswith('.names') and path in ALLOWED_PATHS.values():
        with open(path, 'rt') as f:
            return f.read().rstrip('\n').split('\n')
    return None

def getOutputsNames(network):
    layersNames = network.getLayerNames()
    return [layersNames[i[0] - 1] for i in network.getUnconnectedOutLayers()]

def drawPred(frame, classes, classId, conf, left, top, right, bottom):
    if classes[classId] not in CLASSES_INTERESTED: return

    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    
    label = '%.2f' % conf
      
    if classes:
        #print(f"classID: {classId}") -> Statystyki
        label = '%s:%s' % (classes[classId], label) if classes[classId] in CLASSES_INTERESTED else None

    
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

def postProcess(frame, classes, outs):
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
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classes, classIds[i], confidences[i], left, top, left + width, top + height)

def getVideoCapture(path):
    if not os.path.isfile(path):
        sys.exit(1)
    else:
        return cv.VideoCapture(path)

def processCapture(cap, classes, net, vid_writer):
    fps = FPS().start()
    while cv.waitKey(1) < 0:
        
        grabbed, frame = cap.read()

        frame = imutils.resize(frame, width=1080)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])

        #print(f"Progress: {int(cap.get(cv2.CAP_PROP_POS_FRAMES))/TOTAL_FRAMES_NUM}")
        #print(f"Frames per second: {int(cv.CAP_PROP_FPS)}")
        
        if (cv.waitKey(20) & 0xFF == ord('q')) or not grabbed:
            break
        
        blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False) 

        net.setInput(blob)

        outs = net.forward(getOutputsNames(net))

        postProcess(frame, classes, outs)

        vid_writer.write(frame.astype(np.uint8))

        cv.imshow("Frame", frame)
        cv.waitKey(1)
        fps.update()

    fps.stop()


if __name__ == "__main__": 
    main("source/okej.avi")