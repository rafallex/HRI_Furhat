from furhat_realtime_api import FurhatClient
from datetime import datetime
import csv
import re
import time
from openai_helper import OpenAIHelper
#from facial_gestures import play_expression

ai = OpenAIHelper()

ROBOT_IP = "127.0.0.1"
AUTH_KEY = None

CONDITION = "empathetic"     # change to "neutral" for condition 2


def connect_furhat():
    if AUTH_KEY:
        furhat = FurhatClient(ROBOT_IP, auth_key=AUTH_KEY)
    else:
        furhat = FurhatClient(ROBOT_IP)

    furhat.connect()
    furhat.request_voice_config(name="Emma", language="en-GB", input_language=True)
    return furhat


def speak(furhat, text):
    print(f"\n[FURHAT]: {text}")
    furhat.request_speak_text(text, wait=True)

def normalize_expression(expression):
    expression = str(expression).lower().strip()
    expression = expression.replace("-", "_").replace(" ", "_").replace(".", "")

    aliases = {
        "sad": "supportive_sad",
        "supportive": "supportive_sad",
        "supportive_sad": "supportive_sad",
        "concern": "concerned",
        "concerned": "concerned",
        "smile": "gentle_smile",
        "gentle_smile": "gentle_smile",
        "happy": "encouraging",
        "encouraging": "encouraging",
        "reflective": "reflective",
        "neutral": "neutral",
    }

    return aliases.get(expression, "reflective")

def safe_gesture(furhat, name):
    try:
        print(f"[GESTURE] Trying: {name}")
        furhat.request_gesture_start(name=name)
        time.sleep(1)
    except Exception as e:
        print(f"[GESTURE ERROR] {name}: {e}")

def play_expression(furhat, expression):

    print(f"[PLAY EXPRESSION] {expression}")

    if expression == "supportive_sad":
        furhat.request_gesture_start("ExpressSad", wait=False)

    elif expression == "concerned":
        furhat.request_gesture_start("ExpressSad", wait=False)

    elif expression == "gentle_smile":
        furhat.request_gesture_start("Smile", wait=False)

    elif expression == "encouraging":
        furhat.request_gesture_start("Smile", wait=False)

    elif expression == "reflective":
        furhat.request_gesture_start("Smile", wait=False)

    else:
        print("[NO GESTURE]")

def listen(furhat):
    print("\n[LISTENING...]")

    response = furhat.request_listen_start()

    if response is None:
        print("[USER]: <NO RESPONSE>")
        return ""

    response = str(response)

    print(f"[USER]: {response}")

    return response


def empathetic_reaction(furhat, user_text):
    text = user_text.lower()

    if any(word in text for word in ["bad", "sad", "stressed", "tired", "anxious", "lonely"]):
        furhat.request_gesture_start(name="ExpressSad")
        speak(furhat, "I'm sorry to hear that. That sounds difficult. Thank you for sharing it with me.")
    elif any(word in text for word in ["good", "happy", "great", "fine", "okay", "better"]):
        furhat.request_gesture_start(name="Smile")
        speak(furhat, "I'm glad to hear that. It is nice that you are noticing positive moments.")
    else:
        furhat.request_gesture_start(name="Nod")
        speak(furhat, "Thank you for telling me. It is helpful to take a moment to reflect on that.")


def neutral_reaction(furhat):
    speak(furhat, "Thank you. Let us continue.")


def ask_question(furhat, question, condition):
    print("\n" + "=" * 60)
    print(f"[QUESTION]: {question}")
    print("=" * 60)

    speak(furhat, question)
    time.sleep(0.5)
    answer = listen(furhat)

    print("\n[OPENAI] Generating response...")

    robot_response = ai.generate_robot_response(answer, condition)

    robot_reply = robot_response["reply"]
    expression = robot_response["expression"]

    print(f"[OPENAI RESPONSE]: {robot_reply}")
    print(f"[OPENAI EXPRESSION]: {expression}")

    if condition == "empathetic":
        #furhat.request_gesture_start("ExpressSad", wait=False)
        if expression == "supportive_sad":
            furhat.request_gesture_start("ExpressSad", wait=False)
        elif expression == "concerned":
            furhat.request_gesture_start("ExpressSad", wait=False)
        elif expression == "gentle_smile":
            furhat.request_gesture_start("Smile", wait=False)
        elif expression == "encouraging":
            furhat.request_gesture_start("Smile", wait=False)
            time.sleep(0.8)
            furhat.request_gesture_start("Nod", wait=False)
        elif expression == "reflective":
            furhat.request_gesture_start("Surprise", wait=False)
            time.sleep(0.8)
            furhat.request_gesture_start("Smile", wait=False)
        else:
            print("[NO GESTURE]")
        #play_expression(furhat, expression)
    else:
        furhat.request_gesture_start("Smile", wait=False)
        #play_expression(furhat, "neutral")
    time.sleep(0.3)
    speak(furhat, robot_reply)

    return answer

# def ask_question(furhat, question, condition):
#     speak(furhat, question)
#     answer = listen(furhat)
#
#     if condition == "empathetic":
#         empathetic_reaction(furhat, answer)
#     else:
#         neutral_reaction(furhat)
#
#     return answer


def save_session(condition, answers):
    filename = "session_data.csv"
    timestamp = datetime.now().isoformat(timespec="seconds")

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for question, answer in answers:
            writer.writerow([timestamp, condition, question, answer])


def run_checkin():
    furhat = connect_furhat()
    answers = []

    try:
        #furhat.request_gesture_start("Smile", wait=False)

        speak(furhat, "Hello. I am Furhat. This is a short wellbeing check-in.")
        speak(furhat, "You can answer briefly, and you can stop at any time.")

        questions = [
            "How are you feeling today?",
            "What is one thing that has affected your mood recently?",
            "Have you done anything enjoyable or relaxing this week?",
            "Have you had contact with friends, family, or someone supportive recently?",
            "What is one small thing you could do for yourself later today?"
        ]

        for question in questions:
            answer = ask_question(furhat, question, CONDITION)
            answers.append((question, answer))
            time.sleep(0.5)

        speak(furhat, "Thank you for doing this check-in with me.")
        speak(furhat, "Remember, I am not a replacement for professional support. If you need help, please contact student health services or someone you trust.")

        save_session(CONDITION, answers)

    finally:
        furhat.request_face_reset()
        furhat.disconnect()


if __name__ == "__main__":
    time.sleep(2)
    run_checkin()