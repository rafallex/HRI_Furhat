'''
This file will control the furhat robot, by connecting to it, disconnecting from it,
speak,listen gestures change led
'''

from furhat_realtime_api import FurhatClient
import numpy as np

class FurhatRobot:
    def __init__(self,host,api):
        self.host=host
        self.api=api
        self.furhat=FurhatClient(host,api)
    
    def connect(self):
        print("connecting to furhat")
        self.furhat.connect()
        print("connected to furhat")
        
    def disconnect(self):
        print("disconnecting from furhat")
        self.furhat.disconnect()
        print("disconnected from furhat")
        
    def configure_voice(self):
        # self.furhat.request_voice_config(name="amy",gender="female",language="en-GB")
        self.furhat.request_voice_config(name="aditi", gender="female", language="en-IN")
    
    def speak(self,robot_utt):
        self.furhat.request_speak_text(robot_utt)
        print(f"robot : {robot_utt}")
    
    
    def listen(self):
        user_utt=self.furhat.request_listen_start()
        print(f"user : {user_utt}")
        return user_utt
        
    def gesture(self,sentiments):
        major_sentiment = max(sentiments, key=sentiments.get)
        print(f"detected sentiment : {sentiments}")
        if major_sentiment == "positive":
            self.furhat.request_gesture_start(name="Smile", intensity=3, duration=2)
        elif major_sentiment == "negative":
            self.furhat.request_gesture_start(name="ExpressSad", intensity=3, duration=2)
        else:
            self.furhat.request_gesture_start(name="Oh", intensity=1, duration=2)
        
    
    def greet_led(self):
        print("changing led to greeting led")
        self.furhat.request_led_set("#F5A623")
    
    def speak_led(self):
        print("changing led to speak led")
        self.furhat.request_led_set("#50C9CE")
    
    def listen_led(self):
        print("changing led to listen led")
        self.furhat.request_led_set("#3A9DA1")
        
    def sentiment_led(self,sentiments):
        print("changing led to according to sentiment detected")
        major_sentiment=max(sentiments,key=sentiments.get)
        print(f"detected sentiment : {sentiments}")
        
        if major_sentiment == "positive":
            self.furhat.request_led_set("#7ED321")
        elif major_sentiment == "negative":
            self.furhat.request_led_set("#E89A3C")
        else:
            self.furhat.request_led_set("#4A90E2")
        
    
    
    
        
    
    