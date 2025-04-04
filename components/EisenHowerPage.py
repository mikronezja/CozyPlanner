import flet as ft 

class EisenHowerPage:
    def __init__(self, tasks):
        self.tasks = tasks
        
    def get_container(self):
        return ft.Text(value="EisenHower Matrix", size = 20)