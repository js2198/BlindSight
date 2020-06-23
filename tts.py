import pyttsx3

def speak(object):
    engine = pyttsx3.init()
    engine.say(object)
    engine.runAndWait()

# import os, time
# from gtts import gTTS 
# from playsound import playsound

# def speak(object):
#   myobj = gTTS(text=object, lang='en-uk') 
#   myobj.save("object.mp3")
#   # print('Speaking...'+ object)
#   playsound('object.mp3')
#   os.remove('object.mp3')