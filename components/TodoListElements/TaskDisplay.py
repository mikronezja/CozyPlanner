import flet as ft 

BGCOLOR = "white"
BORDER_RADIUS = 5
MARGIN = 10

class TaskDisplay: # single task displayed 
    def __init__(self, tasks):
        self.tasks = tasks
        self.task_container = []
        self.task_column = ft.Column(spacing=30)

        for i, task in enumerate(tasks):
            check_box = ft.Checkbox(
                label=task.name, 
                value=task.completed, 
                on_change=lambda e, i=i: self.on_change(i),
                label_position=ft.LabelPosition.LEFT
            )
            self.task_container.append(check_box)
            self.task_column.controls.append(check_box)

        self.container = ft.Container(content=self.task_column, 
                                      border_radius=BORDER_RADIUS,
                                      alignment=ft.alignment.center,
                                      margin=MARGIN)
    
    def task_append(self, task):
        next_index = len(self.task_container)
        check_box = ft.Checkbox(label=task.name, 
                                               value=task.completed, 
                                               on_change=lambda e: self.on_change(next_index),
                                               label_position=ft.LabelPosition.LEFT)
        self.task_container.append(check_box)
        self.task_column.controls.append(check_box)
        self.task_column.update()


    def on_change(self, index):
        self.tasks[index].completed = self.task_container[index].value # updates the values of 
        self.task_container[index].update()

    def set_visible(self, value):
        self.container.visible = value

    def get_container(self):
        return self.container