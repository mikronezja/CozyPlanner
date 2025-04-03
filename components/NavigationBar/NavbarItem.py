import flet as ft 

# going to use the ft.Image class for this
class NavbarItem: 
    def __init__(self, text, color, page_to_link_to, page):
        self.text = text
        self.color = color
        self.page = page
        self.page_to_link_to = page_to_link_to
    
    def get_container(self): # potem cos zaawansowanszego bedzie
        return ft.ElevatedButton(text=self.text,color=self.color, on_click=lambda _: self.page.go(self.page_to_link_to))