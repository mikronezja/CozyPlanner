import flet as ft 
from .HomePageElements.AffirmationButton import AffirmationButton
from .HomePageElements.Tree import Tree

class HomePage:
    def __init__(self):
        self.text_from_ai = ft.Text("") 
        self.affirmation_button = AffirmationButton(self.on_button_click)
        self.text_container = ft.Container(
                    content=self.text_from_ai,
                    bgcolor=ft.Colors.WHITE, 
                    alignment=ft.alignment.center,
                    width=100,
                    visible=False
                    )
        self.tree=Tree()
        self.welcome_text=ft.Container(
            content=ft.Text("Welcome to CosyPlanner!! Click the button to get your daily affirmation!",color='#702106',size=30,text_align=ft.TextAlign.CENTER,),
            alignment=ft.alignment.center,
        )
        

    def on_button_click(self, e):
        affirmation = self.affirmation_button.get_response()
        self.text_from_ai.value = affirmation
        self.text_container.visible = True
        e.page.update()  

    def get_container(self):
        return ft.Container(
            content=ft.Column(controls=[self.welcome_text, ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self.affirmation_button.get_container(),
                            ft.Row(
                                controls=[self.text_container],
                                alignment=ft.alignment.center,
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.tree.get_container()
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )]),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=20,right=20,top=0,bottom=0),
            margin=0
        )