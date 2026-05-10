from groq import Groq
import os
from dotenv import load_dotenv
from prompts import robot_prompt,greeting_prompt,response_prompt
from google import genai
from google.genai import types

load_dotenv()

class GroqLLM:
    def __init__(self):
        self.client=Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model="llama-3.3-70b-versatile"
        self.messages=[{'role':'system',
                       'content':robot_prompt}]
        
    def greet_user(self):
        self.messages.append({'role':'user',
                              'content':greeting_prompt})
        
        llm_response=self.client.chat.completions.create(messages=self.messages,
                                                      model=self.model)
        greeting_response=llm_response.choices[0].message.content
        self.messages.append({'role': 'assistant',
                              'content': greeting_response})
        return greeting_response
    
    def generate_response(self,query):
        
        
        self.messages.append({"role":"user",
                            "content":query})
        ack_query=f'The user responded {query}\n\n{response_prompt}'
        self.messages.append({"role": "user",
                              "content": ack_query})
        llm_response = self.client.chat.completions.create(messages=self.messages,
                                                      model=self.model)
        robot_utt=llm_response.choices[0].message.content
        self.messages.append({"role":"assistant",
                              "content":robot_utt})
        return robot_utt
        


class GeminiLLM:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"
        self.config = types.GenerateContentConfig(
            system_instruction=robot_prompt,
        )
        self.messages = [{'role': 'system', 'content': robot_prompt}]

    def _to_gemini(self):
        role_map = {'user': 'user', 'assistant': 'model'}
        return [
            {'role': role_map[m['role']], 'parts': [{'text': m['content']}]}
            for m in self.messages if m['role'] in role_map
        ]

    def greet_user(self):
        self.messages.append({'role': 'user', 'content': greeting_prompt})

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self._to_gemini(),
            config=self.config,
        )
        greeting_response = response.text

        self.messages.append({'role': 'assistant', 'content': greeting_response})
        return greeting_response

    def generate_response(self, query):
        self.messages.append({'role': 'user', 'content': query})

        ack_query = f'The user responded {query}\n\n{response_prompt}'
        self.messages.append({'role': 'user', 'content': ack_query})

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self._to_gemini(),
            config=self.config,
        )
        robot_utt = response.text

        self.messages.append({'role': 'assistant', 'content': robot_utt})
        return robot_utt