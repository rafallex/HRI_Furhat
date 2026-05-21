# facial_gestures.py
import time

def safe_gesture(furhat, name):
    try:
        print(f"[GESTURE] Trying: {name}")
        furhat.request_gesture_start(name=name, wait=False)
        time.sleep(0.8)
    except Exception as e:
        print(f"[GESTURE ERROR] {name}: {e}")


def play_expression(furhat, expression: str):
    expression = expression or "neutral"

    try:
        furhat.request_face_reset()
        time.sleep(0.2)
    except Exception as e:
        print(f"[FACE RESET ERROR] {e}")

    if expression == "supportive_sad":
        safe_gesture(furhat, "ExpressSad")

    elif expression == "concerned":
        safe_gesture(furhat, "ExpressSad")

    elif expression == "gentle_smile":
        safe_gesture(furhat, "Smile")

    elif expression == "encouraging":
        safe_gesture(furhat, "Smile")

    elif expression == "reflective":
        # Avoid Nod if it does not exist
        safe_gesture(furhat, "Smile")

    else:
        print("[GESTURE] Neutral: no gesture")