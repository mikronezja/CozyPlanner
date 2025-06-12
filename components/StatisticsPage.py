import flet as ft

class StatisticsPage:
    def __init__(self, database):
        self.database = database

    def get_container(self):
        return ft.Container()