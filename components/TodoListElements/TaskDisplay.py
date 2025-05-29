import flet as ft 

BGCOLOR = "white"
BORDER_RADIUS = 5
MARGIN = 10

class TaskDisplay: # single task displayed 
    def __init__(self, database, todays_date):
        # self.tasks = tasks

        self.database = database
        self.todays_date = (todays_date.day, todays_date.month, todays_date.year)

        self.task_container = []
        self.task_column = ft.Column(spacing=30)

        for i, (task_id, date_id, name, desc, completed, urgency, importance) in enumerate(database.get_tasks(*self.todays_date)):
            check_box = ft.Checkbox(
                label=name, 
                value=completed, 
                on_change=lambda e: self.on_change(task_id, i),
                label_position=ft.LabelPosition.LEFT,
                label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_800, size=23)
            )
            self.task_container.append(check_box)
            self.task_column.controls.append(check_box)
        # end for

        self.container = ft.Container(content=self.task_column, 
                                      border_radius=BORDER_RADIUS,
                                      alignment=ft.alignment.top_center,
                                      padding=ft.padding.only(left=30, right=30, top=60, bottom=30),
                                      #alignment=ft.alignment.center,
                                      #margin=MARGIN,
                                      height=600,
                                      width=400,
                                      bgcolor=ft.Colors.TRANSPARENT,
                                      #image=ft.DecorationImage(src="icons/list.png",fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT,alignment=ft.alignment.center)
                                      
                                      )
    
    def task_append(self, name, idx_in_database):
        next_index = len(self.task_container)
        check_box = ft.Checkbox(label=name, 
                                               check_color=ft.Colors.GREEN,
                                               fill_color=ft.Colors.YELLOW,
                                               value=0, 
                                               on_change=lambda e: self.on_change(idx_in_database, next_index),
                                               label_position=ft.LabelPosition.LEFT)
        self.task_container.append(check_box)
        self.task_column.controls.append(check_box)
        self.task_column.update()


    def on_change(self, id, i):
        self.database.change_task_completion(id)
        self.task_container[i].update()

    def set_visible(self, value):
        self.container.visible = value

    def get_container(self):
        return self.container