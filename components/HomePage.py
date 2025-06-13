import flet as ft 
from .HomePageElements.AffirmationButton import AffirmationButton
from random import choice

class HomePage:
    def __init__(self):
        self.text_from_ai = ft.Text(value="", color="#702106", size=16) 
        self.affirmation_button = AffirmationButton(self.on_button_click)
        self.text_container = ft.Container(
                    content=self.text_from_ai,
                    bgcolor=ft.Colors.PINK_100, 
                    alignment=ft.alignment.center,
                    width=100,
                    visible=False
                    )
        # self.tree=Tree()
        self.welcome_text=ft.Container(
            content=ft.Text("Welcome to CosyPlanner!! Click the button to get your daily affirmation!",color='#702106',size=30,text_align=ft.TextAlign.CENTER,),
            alignment=ft.alignment.center,
        )
        self.frog_image = ft.Image(src="icons/frog.png", height=100)
        self.frog = ft.Container(
            content=self.frog_image,
            # padding=ft.Padding(top=100, left=100, right=100, bottom=100),
            visible=False,
            on_hover=self.on_frog_hover,
            offset=ft.Offset(0,0)
       )
        self.frog.animate_offset = ft.Animation(800)
        self.tree_image = ft.Image(
            src="icons/tree.png",
            height=500
        )
        self.tree_container = ft.Container(
            content=self.tree_image,
            on_click=self.on_tree_click,
            on_hover=self._on_tree_hover,
            scale=1.0,
            animate_scale=ft.Animation(20),
            width=500,
            height=500,
            alignment=ft.alignment.center
        )
        
    def _on_tree_hover(self, e: ft.HoverEvent):
        if e.data=="true":
            self.tree_container.scale=1.005
        else:
            self.tree_container.scale=1.0
        self.tree_container.update()

    def on_button_click(self, e):
        affirmation = self.affirmation_button.get_response()
        self.text_from_ai.value = affirmation
        self.text_container.visible = True
        e.page.update()  
    def on_tree_click(self, e):
        self.frog.visible = not self.frog.visible
        self.frog.update()
    def on_frog_hover(self,e: ft.HoverEvent):
        dirs=[-1,0,1]
        if e.data=="true":
            randomdirx=choice(dirs)
            randomdiry=choice(dirs)
            self.frog.offset=ft.Offset(1.0*randomdirx,1.0*randomdiry)
            self.frog.update()
        else:
            self.frog.offset=ft.Offset(0,0)
        self.frog.update()
    # def get_container(self):
    #     return ft.Container(
    #         content=ft.Column(controls=[self.welcome_text, ft.Row(
    #             controls=[
    #                 ft.Column(
    #                     controls=[
    #                         self.affirmation_button.get_container(),
    #                         ft.Row(
    #                             controls=[self.text_container],
    #                             alignment=ft.alignment.center,
    #                         )
    #                     ],
    #                     expand=True,
    #                     alignment=ft.MainAxisAlignment.CENTER
    #                 ),
    #                 self.tree_container
    #             ],
    #             alignment=ft.MainAxisAlignment.CENTER
    #         )]),
    #         expand=True,
    #         alignment=ft.alignment.center,
    #         padding=ft.padding.only(left=20,right=20,top=0,bottom=0),
    #         margin=0
    #     )
    def get_container(self):
        main_content = ft.Container(
            content=ft.Column(
                controls=[
                    self.welcome_text,
                    ft.Row(
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
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            self.tree_container,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=20, right=20, top=0, bottom=0),
            margin=0,
        )

    # Teraz wrzucamy wszystko do Stacka i dodajemy żabę
        return ft.Stack(
            controls=[
                main_content,
                # self.frog
                ft.Container(
                content=self.frog,
                alignment=ft.alignment.center,
                width=100
                    )
            ],
            expand=True,
        )
