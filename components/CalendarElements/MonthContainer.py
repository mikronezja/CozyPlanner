import flet as ft
import calendar
from .DateBox import DayContainer

class MonthContainer:
    def __init__(self, month, year):
        self.month_days = calendar.monthrange(year, month)[1]
        self.starting_weekday = calendar.monthrange(year, month)[0]
        self.days_container = [ DayContainer(day=i,month=month, year=year, on_click=lambda i=i: self.on_click(i)) for i in range(1, self.month_days+1) ]

    def get_container(self):
        column = ft.Column()

        days_of_week = {
            0: "Mo",
            1: "Tu",
            2: "We",
            3: "Th",
            4: "Fr",
            5: "Sa",
            6: "Su",
        }

        header_row = ft.Row()
        for i in range(len(days_of_week)):
            header_row.controls.append(ft.Container(content=ft.Text(days_of_week[i],size=30, color=ft.Colors.BLUE_GREY_800), width=100, height=50))

        column.controls.append(header_row)

        row = ft.Row()
        # dodaje puste pola do poczatku tygodnia
        for _ in range(self.starting_weekday):
            row.controls.append(ft.Container(width=100,height=50))

        for day in self.days_container:
            if len(row.controls) == 7:
                column.controls.append(row)
                row = ft.Row()
            row.controls.append(day)

        if row.controls:
            column.controls.append(row)

        return column
