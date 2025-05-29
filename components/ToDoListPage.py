import flet as ft 
from .TodoListElements.InputTask import InputTask
# from .TodoListElements.Task import Task
from .TodoListElements.TaskDisplay import TaskDisplay
import datetime


button_src="icons/task_button.png"
class ToDoListPage:
    def __init__(self, database):
       self.todays_date = datetime.datetime.now()
       self.database = database

       self.create_task_button=ft.Container(
            content=ft.Image(src=button_src,width=200),
            on_click=self.on_create_button_visible_click,
            on_hover=self._on_hover,
            offset=ft.Offset(0,0)
        )
       
       self.input_task = InputTask(on_input_task_click=lambda name, desc: self.on_input_task_click(name, desc))

       self.task_display = TaskDisplay(self.database, self.todays_date)
    #    self.task_scrollable_container=ft.Container(
    #     content=ft.Column(
    #         controls=[self.task_display.get_container()],
    #         scroll=ft.ScrollMode.AUTO,
    #         expand=True
    #     ),
    #     expand=True
    #    )
       self.task_scrollable_container = ft.Container(
       content=ft.Container(  # wewnętrzny kontener z kolumną zadań
           content=ft.Column(
               controls=[self.task_display.get_container()],
               scroll=ft.ScrollMode.AUTO,
               expand=True
           ),
           height=600,
           width=400,
           padding=ft.padding.only(left=30, right=30, top=50, bottom=50),
           alignment=ft.alignment.top_center,
       ),
       border_radius=5,
       height=600,
       width=400,
       margin=ft.margin.only(left=100,right=100),
       image=ft.DecorationImage(
           src="icons/list.png",
           fit=ft.ImageFit.FILL,
           repeat=ft.ImageRepeat.NO_REPEAT,
           alignment=ft.alignment.center
       ),
       )


       self.right_side=ft.Container(ft.Column(
        controls=[self.create_task_button,self.input_task.get_container()],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
        ),
        margin=ft.margin.only(left=100,right=100)
       )

       self.container=ft.Row(
        controls=[
            self.task_scrollable_container,
            self.right_side
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
       )
    #    self.container = ft.Row( 
    #       controls=[ft.Column(controls=[self.create_task_button, self.input_task.get_container(), self.task_display.get_container()])],
    #        alignment=ft.MainAxisAlignment.CENTER,
    #        expand=True)
       
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
        
    def _on_hover(self, e):
        if e.data=="true":
            self.create_task_button.offset=ft.Offset(0,0.03)
        else:
            self.create_task_button.offset=ft.Offset(0,0)
        self.create_task_button.update()
        
    def on_create_button_visible_click(self, e):
        self.create_task_button.visible = False 
        # self.task_display.set_visible(False)

        self.input_task.reset_field_values()
        self.input_task.set_visible(True)
        self.update_all()

    def on_input_task_click(self, name, desc):
        self.create_task_button.visible = True 
        self.task_display.set_visible(True)

        new_task = (name, desc, self.input_task.task_urgency_slider.value, self.input_task.task_importance_slider.value)
        idx_in_database = self._add_task_to_db_safely(*new_task)


        self.task_display.task_append(name=new_task[0],idx_in_database=idx_in_database)
        self.input_task.set_visible(False)

        self.update_all()

    def update_all(self):
        self.input_task.update()
        self.create_task_button.update()
        self.container.update()

    def get_container(self):
        return self.container