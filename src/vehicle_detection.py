import os
import argparse
import cv2
from imutils.video import FPS
import numpy as np
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Provide a full path to the video")

# os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings", "GrupaC1.avi")
args = vars(ap.parse_args())


ALLOWED_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)),   "models", "car.xml"),
    # os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "truck.xml"),
    # os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "motorcycle.xml")
]

# Trained XML - Car classifier
car_cascade = cv2.CascadeClassifier(ALLOWED_PATHS[0])
# Trained XML - Truck classifier
# truck_cascade = cv2.VideoCapture(ALLOWED_PATHS[1])
# Trained XML  - Motorcycle classifier
# motorcycle_cascade = cv2.VideoCapture(ALLOWED_PATHS[2])


stream = cv2.VideoCapture(args["video"])
fps = FPS().start()

TOTAL_FRAMES_NUM = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
print(TOTAL_FRAMES_NUM)
while True:

    grabbed, frame = stream.read()

    if not grabbed:
        break

    frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])

    #cars = car_cascade.detectMultiScale(frame, 1.1, 2)
    
    #for (x, y, w, h) in cars:
    #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    print(f"Progress: {int(stream.get(cv2.CAP_PROP_POS_FRAMES))/TOTAL_FRAMES_NUM}")
    print(f"Frames per second: {int(cv2.CAP_PROP_FPS)}")
    
    if (cv2.waitKey(20) & 0xFF == ord('q')):
        break

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    fps.update()

    

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

stream.release()
cv2.destroyAllWindows()

# Logging -> logi do pliku .log



