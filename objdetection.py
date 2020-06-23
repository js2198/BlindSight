# Usage: python objdetection.py --prototxt deploy.prototxt.txt --model deploy.caffemodel

from imutils.video import VideoStream, FPS
import numpy as np
import argparse, imutils, time, cv2
from tts import speak

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


# initialize the list of class labels for which the model is trained
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# load serialized model from disk
net = cv2.dnn.readNetFromCaffe( args["prototxt"], args["model"])

# Initialize variables & constants
vs = VideoStream(src=0).start()
fps = FPS().start()
flag = False # Camera will keep running until this flag is set to True
objectsFound = []
NUMBER_OF_OBJECTS_TO_BE_DETECTED = 5

# loop over the frames from the video stream
while True:
    if flag == True:
        break    
    # grab the frame resize it and convert it to a blob
    frame = vs.read()
    cv2.imshow('Frame',frame)
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # obtain the detections and predictions fro the blob
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # filter out weak detections by ensuring the confidence is greater than the minimum confidence
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            idx = int(detections[0, 0, i, 1])            
            objectFound = CLASSES[idx]
            
            print(objectFound + " detected")
            speak(objectFound)
            
            if objectFound not in objectsFound:
                objectsFound.append(objectFound)
            if len(objectsFound) >= NUMBER_OF_OBJECTS_TO_BE_DETECTED:
                flag = True
        
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            flag = True
            break

        fps.update()

fps.stop()
cv2.destroyAllWindows()
vs.stop()

print("Objects Found: ", objectsFound)

# Speak objects found
# for object in objectsFound:
#     speak(object)
