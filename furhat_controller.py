from furhat_realtime_api import FurhatClient
from datetime import datetime
import csv
import re
import time
from openai_helper import OpenAIHelper

ai = OpenAIHelper()

ROBOT_IP = "127.0.0.1"       # change to Furhat IP if not using virtual Furhat
AUTH_KEY = None              # put your key here if authentication is enabled

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
        furhat.request_gesture_start("ExpressSad", wait=False)
        speak(furhat, "I'm sorry to hear that. That sounds difficult. Thank you for sharing it with me.")
    elif any(word in text for word in ["good", "happy", "great", "fine", "okay", "better"]):
        furhat.request_gesture_start("Smile", wait=False)
        speak(furhat, "I'm glad to hear that. It is nice that you are noticing positive moments.")
    else:
        furhat.request_gesture_start("Nod", wait=False)
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

    robot_reply = ai.generate_robot_response(answer, condition)

    print(f"[OPENAI RESPONSE]: {robot_reply}")

    if condition == "empathetic":
        furhat.request_gesture_start("Nod", wait=False)

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
        furhat.request_gesture_start("Smile", wait=False)

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
    run_checkin()