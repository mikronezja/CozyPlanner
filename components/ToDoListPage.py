import flet as ft 
from .TodoListElements.InputTask import InputTask
from .TodoListElements.Task import Task
from .TodoListElements.TaskDisplay import TaskDisplay
import datetime

button_src="icons/task_button.png"
class ToDoListPage:
    def __init__(self, tasks, database):
       self.todays_date = datetime.datetime.now()
    #    self.tasks = tasks 
       self.database = database

    #    self.create_task_button = ft.ElevatedButton(
    #        text="Create task", 
    #        on_click=self.on_create_button_visible_click, 
    #        visible=True)
       
       self.input_task = InputTask(on_input_task_click=lambda name, desc: self.on_input_task_click(name, desc))

       self.task_display = TaskDisplay(self.database, self.todays_date)

       self.container = ft.Row( 
           controls=[ft.Column(controls=[self.create_task_button, self.input_task.get_container(), self.task_display.get_container()])],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True)
       
    def _add_task_to_db_safely(self, name, desc, urgency, importance):
        try:
            task_id = self.database.add_task(
                day=self.todays_date.day,
                month=self.todays_date.month,
                year=self.todays_date.year,
                name=name,
                desc=desc,
                urgency=urgency,
                importance=importance,
            )
            print(f"Task zostal dodany do bazy danych {task_id}")
            return task_id
        except Exception as db_error:
            print(f"[ERROR] w dodawaniu do bazy danych: {db_error}")
            return None

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

    def on_input_task_click(self, name, desc):
        self.create_task_button.visible = True 
        self.task_display.set_visible(True)
        ###
        #new_task = Task(name, desc, self.input_task.task_importance.value, self.input_task.task_urgency.value)

        new_task = (name, desc, self.input_task.task_urgency.value, self.input_task.task_importance.value)
        idx_in_database = self._add_task_to_db_safely(*new_task)

        # self.tasks.append(new_task)
        self.task_display.task_append(name=new_task[0],idx_in_database=idx_in_database)
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