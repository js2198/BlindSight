# BlindSight
BlindSight provides virtual eye for the blind people.
Using camera this app detects object in the surrounding and speaks the object detected in real-time.

It can also be used with Raspberry-Pi using camera and speaker module along with it, so that solution becomes portable.

### Usage
* To Run along with UI, run app.py and access localhost.
* To Run only python script, run objdetection.py along with parameters as shown below: <br />
      python objdetection.py --prototxt deploy.prototxt.txt --model deploy.caffemodel
