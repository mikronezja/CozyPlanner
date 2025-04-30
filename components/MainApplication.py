from .NavigationBar.Navbar import Navbar
import flet as ft 
from .ToDoListPage import ToDoListPage
from .EisenHowerPage import EisenHowerPage
from .PomodoroPage import PomodoroPage
from .HomePage import HomePage
from .CalendarPage import CalendarPage
import icons

BGCOLOR = "#a7dfff"
BGIMAGE="background/bgpng.png"
class MainApplication:
    def __init__(self, page : ft.Page):
        self.page = page
        self.tasks = [] # poki co takie rozwiazanie - potem moze jakas bazka 
    
    def route_change(self, e : ft.RouteChangeEvent) -> None:
        self.page.views.clear()
        navbar_container = Navbar( [("Home","/", "icons/home_icon.png"),
                                    ("Eisenhower Matrix","/eisenhwr","icons/eisenhower_icon.png"), 
                                    ("To-do list","/todo", "icons/todo_icon.png"), 
                                    ("Pomodoro","/pmdr", "icons/clock_icon.png"), 
                                    ("Calendar","/clndr","icons/calendar.png")], 
                        self.page.window.width, self.page).get_container()
        
        # navbar_container = Navbar( [("Home","/"),("Eisenhower Matrix","/eisenhwr"), ("To-do list","/todo"), ("Pomodoro","/pmdr")], 
        #                 self.page.window.width, self.page).get_container()
        route_map = {
            "/": HomePage().get_container(),
            "/eisenhwr":EisenHowerPage(self.tasks).get_container(),
            "/pmdr":PomodoroPage().get_container(),
            "/todo":ToDoListPage(self.tasks).get_container(),
            "/clndr":CalendarPage().get_container()
        }

        content = route_map.get(e.route)

        #background = ft.Image(src=BGIMAGE, fit=ft.ImageFit.COVER, width=self.page.window.width, height=self.page.window.height)

        self.page.views.append(
        ft.View(
            
            route=e.route,
            bgcolor=ft.Colors.TRANSPARENT,
            decoration=ft.BoxDecoration(image=ft.DecorationImage(src='background/bgpng.png',fit=ft.ImageFit.COVER)),
            controls=[navbar_container] + ([content] if content else []))
        #     controls=[
        #             ft.Stack(  # Stack pozwala na warstwowanie elementów
        #                 controls=[background, navbar_container] + ([content] if content else [])
        #             )
        #         ]
        # ))
        )

        self.page.update()

    def display(self): # ALWAYS REMEMBER TO UPDATE THE PAGE!
        self.page.on_route_change = self.route_change
        self.page.go(self.page.route)
        