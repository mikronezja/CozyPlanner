import os
from dotenv import load_dotenv
import google.generativeai as ai
import flet as ft

class AffirmationButton:
    def __init__(self,on_click_function):
        load_dotenv()
        self.on_click_function = on_click_function
        api_key = os.getenv("OPENAI_API_KEY")
        ai.configure(api_key=api_key)
    def get_container(self):
        return ft.FilledButton(text="Affirmation",bgcolor=ft.Colors.PINK_200, on_click=self.on_click_function)
    def get_response(self):
        model = ai.GenerativeModel("gemini-1.5-flash")
        prompt = "You are a kind motivational spreaker give me a unique short positive affirmation"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Error during text generation"
