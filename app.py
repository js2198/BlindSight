from flask import Flask, url_for, redirect, render_template, Response
from tts import speak
import threading
from imutils.video import VideoStream, FPS
import numpy as np
import imutils, cv2, json, base64

app = Flask(__name__)
vs = None
fps = None
 # load serialized model from disk
net = cv2.dnn.readNetFromCaffe( 'deploy.prototxt.txt', 'deploy.caffemodel' ) 
# initialize the list of class labels for which the model is trained
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    global vs, fps, txt
    vs = VideoStream(src=0).start()
    fps = FPS().start() 
   
    while True:
        # grab the frame resize it and convert it to a blob
        _frame = vs.read()
        frame = imutils.resize(_frame, width=400)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        
        # obtain the detections and predictions fro the blob
        net.setInput(blob)
        detections = net.forward()
        objectFound = None
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # filter out weak detections by ensuring the confidence is greater than the minimum confidence
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.2:  
                idx = int(detections[0, 0, i, 1])            
                objectFound = CLASSES[idx]
                print(objectFound + " detected")  
            fps.update()
        
        # t = threading.Thread(target=speak, args=(objectFound,))
        
        ret, jpeg = cv2.imencode('.jpg', _frame)    
        only_image = base64.b64encode(jpeg.tobytes())
        if objectFound is not None:
            yield json.dumps({'obj': objectFound,
                            'frame': str(only_image) })
        
        # t.start() 
        # t.join()

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/stop_video')
def stop_video():
    global vs, fps
    fps.stop() 
    vs.stream.release()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)