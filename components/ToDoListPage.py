import flet as ft 
from .TodoListElements.InputTask import InputTask
from .TodoListElements.Task import Task

class ToDoListPage:
    def __init__(self, tasks, page):
       
       self.tasks = tasks 
       self.page = page

       self.create_task_button = ft.ElevatedButton(
           text="Create task", 
           on_click=self.on_create_button_visible_click, 
           visible=True)
       
       self.input_task = InputTask(lambda name, desc: self.on_input_task_click(name, desc)).get_container() ## !!!
       self.input_task.visible = False
       
       self.container = ft.Column([self.create_task_button, self.input_task])

    def on_create_button_visible_click(self, e):
        self.create_task_button.visible = False 
        self.input_task.visible = True
        self.page.update()

    def on_input_task_click(self, name : str, desc : str):
        self.create_task_button.visible = True 
        self.input_task.visible = False
        self.tasks.append(Task(name, desc))
        self.page.update()
        print(len(self.tasks))

    def get_container(self):
        return self.container