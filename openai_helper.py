import os
from openai import OpenAI
from dotenv import load_dotenv


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
            You are generating short neutral robot replies for a university wellbeing check-in.
            Do not sound emotional. Do not give advice. Keep it short.
            """
        else:
            system_prompt = """
            You are generating short empathetic robot replies for a university wellbeing check-in.
            Be warm, supportive, and careful.
            Do not diagnose. Do not act like a therapist.
            Encourage the student gently.
            Keep it 1-2 sentences.
            """

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"The student said: {user_answer}"
                }
            ]
        )

        reply = response.output_text

        print("\n[OPENAI RAW RESPONSE]")
        print(reply)

        return reply
        #return response.output_text