'''

This file will control the furhat robot, by connecting to it, disconnecting from it,
speak,listen gestures change led
'''

from furhat_realtime_api import FurhatClient

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
        self.furhat.request_voice_config(name="amy",gender="female",language="en-GB")
        
    
    def speak(self,robot_utt):
        self.furhat.request_speak_text(robot_utt)
        print(f"robot : {robot_utt}")
    
    
    def listen(self):
        user_utt=self.furhat.request_listen_start()
        print(f"user : {user_utt}")
        return user_utt
        
    def gesture(self,sentiment):
        pass
    
    def greet_led(self):
        print("changing led to greeting led")
        self.furhat.request_led_set("#F5A623")
    
    def speak_led(self):
        print("changing led to speak led")
        self.furhat.request_led_set("#50C9CE")
    
    def listen_led(self):
        print("changing led to listen led")
        self.furhat.request_led_set("#3A9DA1")
    
    
    
        
    
    