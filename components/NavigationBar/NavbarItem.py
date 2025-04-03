import flet as ft 

# going to use the ft.Image class for this
class NavbarItem: 
    def __init__(self, text, color, size):
        self.text = text
        self.color = color
        self.size = size
    
    def get_container(self): # potem cos zaawansowanszego bedzie
        return ft.Text(value=self.text,color=self.color, size=self.size)