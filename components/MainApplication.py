from .NavigationBar.Navbar import Navbar
import flet as ft 
from .ToDoListPage import ToDoListPage
from .EisenHowerPage import EisenHowerPage
from .PomodoroPage import PomodoroPage

BGCOLOR = "#a7dfff"

class MainApplication:
    def __init__(self, page : ft.Page):
        self.page = page
        self.tasks = [] # poki co takie rozwiazanie - potem moze jakas bazka 
    
    def route_change(self, e : ft.RouteChangeEvent) -> None:
        self.page.views.clear()
        navbar_container = Navbar( [("Home","/"),("Eisenhower Matrix","/eisenhwr"), ("To-do list","/todo"), ("Pomodoro","/pmdr")], 
                        self.page.window.width, self.page).get_container()
        
        route_map = {
            "/": None,
            "/eisenhwr":EisenHowerPage(self.tasks).get_container(),
            "/pmdr":PomodoroPage().get_container(),
            "/todo":ToDoListPage(self.tasks).get_container()
        }

        content = route_map.get(e.route)
    
        self.page.views.append(
        ft.View(
            route=e.route,
            bgcolor=BGCOLOR,
            controls=[navbar_container] + ([content] if content else []))
        )

        self.page.update()

    def display(self): # ALWAYS REMEMBER TO UPDATE THE PAGE!
        self.page.on_route_change = self.route_change
        self.page.go(self.page.route)
        