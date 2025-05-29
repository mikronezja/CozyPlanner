import flet as ft 

# going to use the ft.Image class for this
class NavbarItem(ft.Container): 
    def __init__(self, text, color, page_to_link_to, page,icon):
        super().__init__()
        
        self.hover_color = color
        self.page = page
        self.page_to_link_to = page_to_link_to

        self.icon=ft.Image(src=icon,height=50,width=50)
        self.label=ft.Text(text,size=16,weight=ft.FontWeight.BOLD, color='#702106')

        self.content=ft.Column(
            controls=[self.icon,self.label],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        self.bgcolor=ft.Colors.TRANSPARENT
        self.padding=10
        self.border_radius=8
        self.animate_bgcolor=300
        self.on_hover=self._on_hover
        self.on_click=self._on_click
        self.height=150
        self.width=150

        #animacje
        self.scale=1.0
        self.animate_scale=70 # czas animacji
        # self.elevation=0
        # self.animate_elevation=50
        
        

    def _on_hover(self,e):
        if e.data=="true":
            self.bgcolor=self.hover_color
            self.scale=1.3
            # self.elevation=12
        else:
            self.bgcolor=ft.Colors.TRANSPARENT
            self.scale=1.0
            # self.elevation=0
        #self.page.update()
        self.update()


    def _on_click(self, e):
        self.page.go(self.page_to_link_to)

    # # def get_container(self):
    # #     return ft.ElevatedButton(text=self.text,color=self.color, on_click=lambda _: self.page.go(self.page_to_link_to))
    # def get_container(self):
    #     return ft.GestureDetector(
    #         on_tap=lambda _: self.page.go(self.page_to_link_to),
    #         content=ft.Column(
    #             controls=[
    #                 self.icon,
    #                 ft.Text(self.text, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800)
    #             ],
    #             alignment=ft.MainAxisAlignment.CENTER,
    #             horizontal_alignment=ft.CrossAxisAlignment.CENTER
    #         )
    #     )

