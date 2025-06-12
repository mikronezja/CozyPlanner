import flet as ft
import datetime
from .CalendarElements.MonthContainer import MonthContainer
from .Enums.Month import Month

class CalendarPage:
    def __init__(self, database):
        self.database = database
        todays_date = datetime.datetime.now()

        self.displayed_year = ft.Text(value=todays_date.year)
        self.displayed_month = ft.Text(todays_date.month)
        self.displayed_day = ft.Text(todays_date.day)
        self.month_text = ft.Text(value=Month(todays_date.month).name)

        self.year_nav_row = ft.Row(
            controls=[
                ft.Button(text="<-", on_click=lambda _: self.change_year(-1)),
                self.displayed_year, 
                ft.Button(text="->", on_click=lambda _: self.change_year(1))
            ],
            alignment=ft.alignment.center
        )
        
        self.month_nav_row = ft.Row(
            controls=[
                ft.Button(text="<-", on_click=lambda _: self.change_month(-1)), 
                self.month_text, 
                ft.Button(text="->", on_click=lambda _: self.change_month(1))
            ],
            alignment=ft.alignment.center
        )

        self.month_container = MonthContainer(
            database, 
            year=int(self.displayed_year.value), 
            month=int(self.displayed_month.value),
            higher_on_click=lambda e: self.__higher_on_click(e),
            show_nav_callback=self.show_navigation
        ).get_container()
        
        self.month_row = ft.Row(controls=[self.month_container])
        
        self.calendar_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.year_nav_row,
                    self.month_nav_row,
                    self.month_row
                ], 
                expand=True
            ),
            expand=True
        )

    def get_container(self):
        return self.calendar_container
    
    def __higher_on_click(self, e):
        self.year_nav_row.visible = False
        self.month_nav_row.visible = False
        self.calendar_container.update()

    def show_navigation(self):
        self.year_nav_row.visible = True
        self.month_nav_row.visible = True
        self.calendar_container.update()

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
        self.month_text.value = Month(month).name
        
        new_month_container = MonthContainer(
            month=month, 
            year=year, 
            database=self.database,
            higher_on_click=lambda e: self.__higher_on_click(e),
            show_nav_callback=self.show_navigation
        ).get_container()
        
        self.month_row.controls = [new_month_container]
        self.month_container = new_month_container
        
        self.calendar_container.update()
    
    def change_year(self, value):
        self.displayed_year.value = str(int(self.displayed_year.value) + value)
        
        new_month_container = MonthContainer(
            month=int(self.displayed_month.value), 
            year=int(self.displayed_year.value),
            database=self.database,
            higher_on_click=lambda e: self.__higher_on_click(e),
            show_nav_callback=self.show_navigation
        ).get_container()
        
        self.month_row.controls = [new_month_container]
        self.month_container = new_month_container
        
        self.calendar_container.update()