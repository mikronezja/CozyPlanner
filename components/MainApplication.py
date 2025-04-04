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
        
        ## Home page
        if e.route == "/": 
            self.page.views.append(
                ft.View(
                    route=e.route,
                    bgcolor= BGCOLOR,
                    controls=[navbar_container])
            )
        ## Pomodoro Page
        if e.route == "/pmdr":
            self.page.views.append(
                ft.View(
                    route=e.route,
                    bgcolor= BGCOLOR,
                    controls=[navbar_container, PomodoroPage().get_container()])
            )

        ## EisenHower Page
        if e.route == "/eisenhwr":
            self.page.views.append(
                ft.View(
                    route=e.route,
                    bgcolor= BGCOLOR,
                    controls=[navbar_container, EisenHowerPage().get_container()])
            )

        ## To do list Page
        if e.route == "/todo":
            self.page.views.append(
                ft.View(
                    route=e.route,
                    bgcolor= BGCOLOR,
                    controls=[navbar_container, ToDoListPage(self.tasks).get_container()])
            )

        self.page.update()

    def display(self): # ALWAYS REMEMBER TO UPDATE THE PAGE!
        self.page.on_route_change = self.route_change
        self.page.go(self.page.route)
        