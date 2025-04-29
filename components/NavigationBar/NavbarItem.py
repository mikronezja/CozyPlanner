import flet as ft 

# going to use the ft.Image class for this
class NavbarItem: # moze dizedziczyc po ft.ElevatedButton! 
    def __init__(self, text, color, page_to_link_to, page,icon):
        super().__init__()
        self.text = text
        self.color = color
        self.page = page
        self.page_to_link_to = page_to_link_to
        self.icon=ft.Image(src=icon,height=50,width=50)
        
    # def get_container(self):
    #     return ft.ElevatedButton(text=self.text,color=self.color, on_click=lambda _: self.page.go(self.page_to_link_to))
    def get_container(self):
        return ft.GestureDetector(
            on_tap=lambda _: self.page.go(self.page_to_link_to),
            content=ft.Column(
                controls=[
                    self.icon,
                    ft.Text(self.text, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    #     self.shadow_box=ft.Container(
    #         content=ft.Column(
    #             controls=[
    #                 self.icon,
    #                 ft.Text(self.text, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800)
    #             ],
    #             alignment=ft.MainAxisAlignment.CENTER,
    #             horizontal_alignment=ft.CrossAxisAlignment.CENTER
    #         ),
    #         animate=ft.AnimationCurve.EASE_IN_OUT,
    #         shadow=None,
    #         border_radius=8,
    #         padding=10
    # )
    
    # def on_hover(self,e):
    #     if e.data=="true":
    #         self.shadow_box.shadow=ft.BoxShadow(
    #             blur_radius=12,
    #             color=ft.colors.GREY_400,
    #             offset=ft.Offset(0,4)
    #         )
    #     else:
    #         self.shadow_box.shadow=None
    #     self.shadow_box.update()

    # def get_container(self):
    #     return ft.MouseRegion(
    #         on_hover=self.on_hover,
    #         cursor=ft.MouseCursor.CLICK,
    #         content=ft.GestureDetector(
    #             on_tap=lambda _: self.page.go(self.page_to_link_to),
    #             content=self.shadow_box
    #         )
    #     )