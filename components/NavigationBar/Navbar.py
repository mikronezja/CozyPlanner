import flet as ft 
from .NavbarItem import NavbarItem

TEXT_COLOR = "#f8fdfe"
TEXT_SIZE = 10
NAVBAR_HEIGHT = 60
SPACING = 20

class Navbar: 
    def __init__(self, pages_list, screen_width):
       self.text_container_list =  [ NavbarItem(text, TEXT_COLOR, TEXT_SIZE).get_container() for text in pages_list ] 

       self.navbar_item_list = ft.Row( 
           controls=self.text_container_list, 
           alignment=ft.MainAxisAlignment.CENTER,
           spacing=SPACING
        )
       
       self.container = ft.Container( 
           content = ft.Stack( 
               controls=[ft.Container(bgcolor="black",expand=True), 
                         ft.Container( content=self.navbar_item_list, 
                                      alignment=ft.alignment.center, 
                                      expand=True )
                         ], expand=True 
               ),
           width=screen_width,
           height=NAVBAR_HEIGHT,
           alignment=ft.alignment.center          
        )

    def get_container(self):
        return self.container