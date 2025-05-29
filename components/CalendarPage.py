import flet as ft
import datetime
from .CalendarElements.MonthContainer import MonthContainer

class CalendarPage:
    def __init__(self, database):
        self.database = database
        self.month_class = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        todays_date = datetime.datetime.now()

        self.displayed_year = ft.Text(value=todays_date.year)
        self.displayed_month = ft.Text(todays_date.month)
        self.displayed_day = ft.Text(todays_date.day)
        self.month_text = ft.Text(value=self.month_class[todays_date.month])

        self.month_container = MonthContainer(year=int(self.displayed_year.value), month=int(self.displayed_month.value)).get_container()
        self.calendar_container = ft.Container(
                    content=ft.Column(controls=[
                        ft.Row(controls=[ft.Button(text="<-", on_click= lambda _: self.change_year(-1)),self.displayed_year, ft.Button(text="->", on_click= lambda _:self.change_year(1))],alignment = ft.alignment.center), 
                        ft.Row(controls=[ft.Button(text="<-", on_click=lambda _:self.change_month(-1)), self.month_text, ft.Button(text="->", on_click=lambda _:self.change_month(1)) ]),
                        ft.Row(controls=[self.month_container])
                    ], alignment=ft.alignment.center, expand=True),
                    alignment=ft.alignment.center,
                    expand=True
                )

    def get_container(self):
        return self.calendar_container
    
    def change_month(self, value):
        month = int(self.displayed_month.value) + value
        year = int(self.displayed_year.value)

        if month == 0:
            month = 12
            year -= 1
        elif month == 13:
            month = 1
            year += 1

        self.displayed_month.value = str(month)
        self.displayed_year.value = str(year)
        self.month_text.value = self.month_class[month]
        self.month_container.controls = [MonthContainer(month=month, year=year).get_container()]

        self.calendar_container.update()
    
    def change_year(self, value):
        self.displayed_year.value = str(int(self.displayed_year.value) + value)
        self.month_container.controls = [MonthContainer(month=int(self.displayed_month.value), year=int(self.displayed_year.value)).get_container()]
        self.calendar_container.update()