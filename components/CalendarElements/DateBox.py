import flet as ft
import datetime

class DayContainer(ft.Container):
    def __init__(self, day, month, year, on_click = None):
        super().__init__()
        now = datetime.datetime.now()

        self.text = ft.Text(str(day), size=20, color='#702106' if ( day != now.day or month != now.month or year != now.year )else ft.Colors.BLUE)

        self.content = ft.Column(
            [self.text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.border_radius = 6
        self.on_click = on_click
        self.width = 100
        self.height = 50