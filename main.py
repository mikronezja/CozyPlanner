import flet as ft 
from Components.MainApplication import MainApplication

## main page of the programme
def main(page: ft.Page):
   page.fonts={
      "Pixelify Sans" : "fonts/PixelifySans-VariableFont_wght.ttf"
   }
   page.theme=ft.Theme(font_family="Pixelify Sans",
   # hover_color=ft.Colors.GREEN_900,
   # shadow_color=ft.Colors.GREEN_900,
   # highlight_color=ft.Colors.CYAN_400
   )

   
   main_app = MainApplication(page) # creating a main app page
   main_app.display()


ft.app(target=main)
