import flet as ft 
from .HomePageElements.AffirmationButton import AffirmationButton

class HomePage:
    def __init__(self):
        self.text_from_ai = ft.Text("") 
        self.affirmation_button = AffirmationButton(self.on_button_click)

    def on_button_click(self, e):
        affirmation = self.affirmation_button.get_response()
        self.text_from_ai.value = affirmation
        e.page.update()  

    def get_container(self):
        return ft.Column([
            self.affirmation_button.get_container(),
            self.text_from_ai
        ])