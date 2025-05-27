import flet as ft 
from .NavbarItem import NavbarItem

HOVER_COLOR = ft.Colors.TRANSPARENT
NAVBAR_HEIGHT = 120
SPACING = 50

class Navbar: 
    def __init__(self, pages_list, screen_width, page):
       self.text_container_list =  [ NavbarItem(text, HOVER_COLOR, page_link, page,icon) for text, page_link,icon in pages_list ] 

       self.navbar_item_list = ft.Row( 
           controls=self.text_container_list, 
           alignment=ft.MainAxisAlignment.CENTER,
           spacing=SPACING
        )
       
       self.container = ft.Container( 
           content = ft.Stack( 
               controls=[ft.Container(expand=True,disabled=True), 
                         ft.Container( content=self.navbar_item_list, 
                                      alignment=ft.alignment.center, 
                                      expand=True )
                         ], expand=True 
               ),
           width=screen_width,
           height=NAVBAR_HEIGHT,
           alignment=ft.alignment.center,
           margin=ft.margin.only(left= 0, top=20,right=0, bottom=30)   
        )

    def get_container(self):
        return self.container