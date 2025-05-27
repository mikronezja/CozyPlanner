import flet as ft 
from .TodoListElements.InputTask import InputTask
from .TodoListElements.Task import Task
from .TodoListElements.TaskDisplay import TaskDisplay

button_src="icons/task_button.png"
class ToDoListPage:
    def __init__(self, tasks):
       
       self.tasks = tasks 
       self.create_task_button=ft.Container(
            content=ft.Image(src=button_src,width=200),
            on_click=self.on_create_button_visible_click,
            on_hover=self._on_hover,
            offset=ft.Offset(0,0)
        )

    #    self.create_task_button = ft.ElevatedButton(
    #        text="Create task", 
    #        on_click=self.on_create_button_visible_click, 
    #        visible=True)
       
       self.input_task = InputTask(on_input_task_click=lambda name, desc: self.on_input_task_click(name, desc))

       self.task_display = TaskDisplay(self.tasks)

       self.container = ft.Row( 
           controls=[ft.Column(controls=[self.create_task_button, self.input_task.get_container(), self.task_display.get_container()])],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True)

    def _on_hover(self, e: ft.HoverEvent):
        if e.data=="true":
            self.container.offset=ft.Offset(0,0.03)
        else:
            self.container.offset=ft.Offset(0,0)
        self.container.update()
    def on_create_button_visible_click(self, e):
        self.create_task_button.visible = False 
        self.task_display.set_visible(False)

        self.input_task.reset_field_values()
        self.input_task.set_visible(True)
        self.update_all()

    def on_input_task_click(self, name : str, desc : str):
        self.create_task_button.visible = True 
        self.task_display.set_visible(True)
        ###
        new_task = Task(name, desc, self.input_task.task_importance.value, self.input_task.task_urgency.value)
        self.tasks.append(new_task)
        self.task_display.task_append(new_task)
        ###
        self.input_task.set_visible(False)
        ###
        self.update_all()

    def update_all(self):
        self.input_task.update()
        self.create_task_button.update()
        self.container.update()

    def get_container(self):
        return self.container