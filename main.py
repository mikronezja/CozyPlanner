import flet as ft 
from Components.MainApplication import MainApplication

## main page of the programme
def main(page: ft.Page):
   main_app = MainApplication(page) # creating a main app page
   main_app.display()


ft.app(target=main)