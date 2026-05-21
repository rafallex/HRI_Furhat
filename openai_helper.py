import os
from openai import OpenAI
from dotenv import load_dotenv
import json


class OpenAIHelper:
    def __init__(self, model="gpt-4.1-mini"):
        load_dotenv(override=True)

        api_key = os.getenv("OPENAI_API_KEY")

        print("Loaded key ending with:", api_key[-4:])

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_robot_response(self, user_answer, condition="empathetic"):
        if condition == "neutral":
            system_prompt = """
            You generate neutral robot replies for a university wellbeing check-in.
            Return ONLY valid JSON with:
            {
              "reply": "...",
              "expression": "neutral"
            }
            Keep the reply short. Do not sound emotional. Do not give advice.
            """
        else:
            system_prompt = """
            You generate empathetic robot replies for a university wellbeing check-in.
            Return ONLY valid JSON with:
            {
              "reply": "...",
              "expression": "supportive_sad | gentle_smile | encouraging | concerned | reflective | neutral"
            }

            Choose expression based on the student's answer:
            - supportive_sad: sad, stressed, lonely, tired, anxious
            - concerned: serious negative answer
            - gentle_smile: okay, fine, calm, mildly positive
            - encouraging: happy, proud, successful, relaxed
            - reflective: unclear, mixed, thoughtful
            - neutral: only for neutral condition

            Be warm and supportive.
            Do not diagnose.
            Do not act like a therapist.
            Keep reply 1-2 sentences.
            """

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"The student said: {user_answer}"}
            ]
        )

        raw = response.output_text
        print("\n[OPENAI RAW RESPONSE]")
        print(raw)

        try:
            data = json.loads(raw)
            return {
                "reply": data.get("reply", "Thank you for sharing that with me."),
                "expression": data.get("expression", "neutral")
            }
        except json.JSONDecodeError:
            return {
                "reply": raw,
                "expression": "reflective"
            }