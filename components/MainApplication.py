from .NavigationBar.Navbar import Navbar
import flet as ft 
from .ToDoListPage import ToDoListPage
from .EisenHowerPage import EisenHowerPage
from .PomodoroPage import PomodoroPage
from .HomePage import HomePage
from .CalendarPage import CalendarPage
from .StatisticsPage import StatisticsPage
from .Sounds.Music import Music

from .CalendarElements.CalendarDatabase import DatabaseManager
# import icons

BGCOLOR = "#a7dfff"
BGIMAGE="background/bgpng.png"
class MainApplication:
    def __init__(self, page : ft.Page):
        self.page = page
        self.database = DatabaseManager()
        self.__sound_button = ft.Container(content=ft.Text(), width=100, height=50, image=ft.DecorationImage(src="icons/sound_stop.png"), on_click=self.__change_music_state)
        self.__sound = Music(src='assets/music/pixel_music.wav',page=self.page,to_be_invoked=False,replay=True)
        

    def route_change(self, e : ft.RouteChangeEvent) -> None:
        #self.page.views.clear()
        navbar_container = Navbar( [("Home","/", "icons/home_icon.png"),
                                    ("To-do list","/todo", "icons/todo_icon.png"),
                                    ("Task Matrix","/eisenhwr","icons/eisenhower_icon.png"), 
                                    ("Pomodoro","/pmdr", "icons/clock_icon.png"), 
                                    ("Calendar","/clndr","icons/calendar.png"),
                                    ("Statistics","/sttstcs", "icons/statistics_icon.png")], 
                        self.page.window.width, self.page).get_container()
        
        route_map = {
            "/": HomePage().get_container(),
            "/eisenhwr":EisenHowerPage(self.database).get_container(),
            "/pmdr":PomodoroPage(self.database,self.page).get_container(),
            "/todo":ToDoListPage(self.database).get_container(),
            "/clndr":CalendarPage(self.database).get_container(),
            "/sttstcs":StatisticsPage(self.database).get_container()
        }

        content = route_map.get(e.route)

        self.page.views.append(
        ft.View(
            route=e.route,
            bgcolor=ft.Colors.TRANSPARENT,
            decoration=ft.BoxDecoration(image=ft.DecorationImage(src='background/bgpng.png',fit=ft.ImageFit.COVER)),
            controls=[
                    ft.Column(
                        controls=[
                            navbar_container,
                            ft.Container(
                                content=content if content else ft.Container(),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[self.__sound_button],
                                    alignment=ft.MainAxisAlignment.END
                                ),
                                padding=ft.padding.only(right=20, bottom=20, top=10)
                            )
                        ],
                        expand=True,
                        spacing=0
                    )
                ]
        )
        )
        self.page.update()

    def __change_music_state(self, e):
        if self.__sound.is_playing:
            self.__sound.stop()
            self.__sound_button.image.src = "icons/sound_stop.png"
        else:
            self.__sound.play()
            self.__sound_button.image.src = "icons/sound_playing.png"
        self.page.update()


    def display(self):
        self.page.on_route_change = self.route_change
        self.page.go(self.page.route)
        