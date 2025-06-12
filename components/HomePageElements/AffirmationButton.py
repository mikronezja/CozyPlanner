import os
from dotenv import load_dotenv
import google.generativeai as ai
import flet as ft

icon_src="icons/affirmation_button.png"
class AffirmationButton:
    def __init__(self,on_click_function):
        self.icon_src=icon_src
        load_dotenv()
        self.on_click_function = on_click_function
        api_key = os.getenv("OPENAI_API_KEY")
        ai.configure(api_key=api_key)
        self.container=ft.Container(
            content=ft.Image(src=self.icon_src,width=200),
            on_click=self.on_click_function,
            on_hover=self._on_hover,
            offset=ft.Offset(0,0)
        )
    def get_container(self):
        # return ft.Container(content=ft.Image(src=icon_src,width=200),on_click=self.on_click_function)
        return self.container
    
    def _on_hover(self, e: ft.HoverEvent):
        if e.data=="true":
            self.container.offset=ft.Offset(0,0.05)
        else:
            self.container.offset=ft.Offset(0,0)
        self.container.update()
    def get_response(self):
        model = ai.GenerativeModel("gemini-1.5-flash")
        prompt = "You are a kind motivational spreaker give me a unique short positive affirmation"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Error during text generation"
