import flet as ft 
import math
import datetime

class EisenHowerPage:
    def __init__(self, tasks, database):
        # self.tasks = tasks
        self.database = database
        
        now = datetime.datetime.now()
        day, month, year = now.day, now.month, now.year
        
        self.tasks = self.database.get_tasks(day,month,year)

        def create_container(name, task_id): # for task
            return ft.Row(controls=[ft.Text(value=name, size = 18, color=ft.Colors.BLUE_GREY_800), 
                                    ft.Checkbox(on_change=lambda e: self.database.change_task_completion(task_id))] ) 

        if len(self.tasks) > 0:
            divider = [ ft.Column(spacing=10) for _ in range(4) ] 

            for (task_id, date_id, name, desc, completed, urgency, importance) in self.tasks:
                if not completed:
                    container = []
                    match importance:
                        case 0:
                            if urgency == 0:
                                container = divider[0]
                            else:
                                container = divider[1]
                        case 1:
                            if urgency == 0:
                                container = divider[2]
                            else:
                                container = divider[3]
                    container.controls.append(create_container(name,task_id))
            

            top_labels = ft.Row([
            ft.Container(content=ft.Text("Urgent", size=20, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_800), expand=True, alignment=ft.alignment.center),
            ft.Container(content=ft.Text("Not Urgent", size=20, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_800), expand=True, alignment=ft.alignment.center),
            ])

            top_row = ft.Row(controls=[
                ft.Container(content=divider[3], image=ft.DecorationImage(src="icons/cont/e_yellow.png",fit=ft.ImageFit.FILL), padding=30, expand=True),  # Important, Urgent
                ft.Container(content=divider[2], image=ft.DecorationImage(src="icons/cont/e_green.png",fit=ft.ImageFit.FILL), padding=30, expand=True),    # Important, Not Urgent
            ], expand=True)

            bottom_row = ft.Row(controls=[
                ft.Container(content=divider[1], image=ft.DecorationImage(src="icons/cont/e_blue.png",fit=ft.ImageFit.FILL), padding = 30, expand=True),  # Not Important, Urgent
                ft.Container(content=divider[0], image=ft.DecorationImage(src="icons/cont/e_pink.png",fit=ft.ImageFit.FILL), padding = 30, expand=True)   # Not Important, Not Urgent
            ], expand=True)

            left_labels = ft.Column([
                ft.Container(content=ft.Text("Important", size=20,color=ft.Colors.BLUE_GREY_800, weight=ft.FontWeight.BOLD, rotate=ft.Rotate(angle=-math.pi/2)), expand=True, alignment=ft.alignment.center),
                ft.Container(content=ft.Text("Not Important", size=20,color=ft.Colors.BLUE_GREY_800, weight=ft.FontWeight.BOLD, rotate=ft.Rotate(angle=-math.pi/2)), expand=True, alignment=ft.alignment.center),
            ])

            self.container = ft.Row( [left_labels,
                                    ft.Column(controls=[top_labels,top_row,bottom_row], 
                                    expand=True)], alignment=ft.alignment.center, expand=True )
        else:
            self.container = ft.Container(
                content=ft.Text(value="No tasks have been added",color=ft.Colors.BLUE_GREY_800, size=25),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=50)
                )
    def get_container(self):
        return self.container