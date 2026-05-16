from LLMmodule import GroqLLM
from furhat_client import FurhatRobot
from prompts import questions
from SentimentEmoModule import SentimentDetection,EmotionDectection
import os
from dotenv import load_dotenv
from prompts import questions,greeting_prompt

load_dotenv()

def main():
    #llm object
    llm=GroqLLM()
    
    #create sentiment class and emotion class
    setiment=SentimentDetection()
    emotion=EmotionDectection()  #might use later
    
    #create furhat object and connect to it
    furhat_host='localhost'
    furhat_auth_key=os.getenv('FURHAT_AUTH_KEY')
    furhat = FurhatRobot(furhat_host,furhat_auth_key)
    #connect to furhat
    furhat.connect()
    
    # configure voice
    furhat.configure_voice()
    
    while True:
        #greet
        furhat.greet_led()
        robot_utt=llm.greet_user()
        furhat.speak(robot_utt)
     
        
        for question in questions:
            #ask question
            furhat.speak_led()
            robot_utt=question
            furhat.speak(question)
         
            llm.messages.append({"role":"assistant",
                                 "content":robot_utt})
            
            #listen to user response
            furhat.listen_led()
            user_response=furhat.listen()
            
            #detect the sentiment of user
            user_sentiment=setiment.detect_sentiment(user_response)
            furhat.gesture(user_sentiment)
            furhat.sentiment_led(user_sentiment)
            #acknowledge the user response
            robot_utt=llm.generate_response(user_response)
            #speak the acknowledgement
            furhat.speak(robot_utt)
            
        
        break
        
    furhat.disconnect()
    print("disconnected")
    
if __name__=="__main__":
    main()