import flet as ft 
from .HomePageElements.AffirmationButton import AffirmationButton

class HomePage:
    def __init__(self):
        self.text_from_ai = ft.Text("") 
        self.affirmation_button = AffirmationButton(self.on_button_click)
        self.text_container = ft.Container(
                    content=self.text_from_ai,
                    bgcolor=ft.colors.WHITE, 
                    alignment=ft.alignment.center,
                    width=100,
                    visible=False
                    )

    def on_button_click(self, e):
        affirmation = self.affirmation_button.get_response()
        self.text_from_ai.value = affirmation
        self.text_container.visible = True
        e.page.update()  

    def get_container(self):
        return ft.Column(
        controls=[
            self.affirmation_button.get_container(),
            ft.Row(
                controls=[self.text_container],
                alignment=ft.alignment.center,
            )
        ],
    )