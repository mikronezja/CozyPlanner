import flet as ft
import calendar
import datetime
from .CalendarElements.MonthContainer import MonthContainer

class CalendarPage:
    def __init__(self):
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
        self.displayed_year = todays_date.year
        self.displayed_month = todays_date.month
        self.displayed_day = todays_date.day

    def get_container(self):
        month_container = MonthContainer(year=self.displayed_year, month=self.displayed_month)
        return ft.Container(
            content=ft.Column(controls=[
                ft.Row(controls=[ft.Button(text="<-"), ft.Text(self.displayed_year), ft.Button(text="->")],alignment = ft.alignment.center), 
                ft.Row(controls=[ft.Button(text="<-"),ft.Text(self.month_class[self.displayed_month]), ft.Button(text="->") ]), 
                ft.Row(controls=[month_container.get_container()])
            ], alignment=ft.alignment.center, expand=True),
            alignment=ft.alignment.center,
            expand=True
        )