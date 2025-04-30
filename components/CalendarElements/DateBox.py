import flet as ft

class DayContainer(ft.Container):
    def __init__(self, day, month, year, on_click = None):
        super().__init__()

        self.text = ft.Text(str(day), size=16)

        self.content = ft.Column(
            [self.text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.border_radius = 6
        self.on_click = on_click
        self.width = 20
        self.height = 20