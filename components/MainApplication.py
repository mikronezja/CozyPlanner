from .NavigationBar.Navbar import Navbar
import flet as ft 

class MainApplication:
    def __init__(self, page):
        self.page = page

    def display(self): # ALWAYS REMEMBER TO UPDATE THE PAGE!
        self.page.bgcolor = "#a7dfff"
        self.page.add(Navbar(["Home","Eisenhower Matrix", "To-do list", "Pomodoro"], self.page.window.width).get_container())
        self.page.views.clear()
        self.page.update()
        