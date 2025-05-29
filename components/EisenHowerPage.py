import flet as ft 
import math
import datetime

class EisenHowerPage:
    def __init__(self, database):
        # self.tasks = tasks
        self.database = database
        
        now = datetime.datetime.now()
        day, month, year = now.day, now.month, now.year
        
        self.tasks = self.database.get_tasks(day,month,year)

        def create_container(name, task_id,divider_index,i): # for task
            return ft.Row(controls=[ft.Text(value=name, size = 18, color=ft.Colors.BLUE_GREY_800), 
                                    ft.Checkbox(on_change=lambda e: self._on_change(task_id,divider_index,i))]) 

        if len(self.tasks) > 0:
            self._divider = [ ft.Column(spacing=10) for _ in range(4) ] 

            for (task_id, date_id, name, desc, completed, urgency, importance) in self.tasks:
                if not completed:
                    divider_index = importance*2 + urgency
                    cont = self._divider[divider_index]

                    cont.controls.append(create_container(name,task_id,divider_index, len(cont.controls)))
            

            top_labels = ft.Row([
            ft.Container(content=ft.Text("Urgent", size=20, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_800), expand=True, alignment=ft.alignment.center),
            ft.Container(content=ft.Text("Not Urgent", size=20, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_800), expand=True, alignment=ft.alignment.center),
            ])

            top_row = ft.Row(controls=[
                ft.Container(content=self._divider[3], image=ft.DecorationImage(src="icons/cont/e_yellow.png",fit=ft.ImageFit.FILL), padding=30, expand=True),  # Important, Urgent
                ft.Container(content=self._divider[2], image=ft.DecorationImage(src="icons/cont/e_green.png",fit=ft.ImageFit.FILL), padding=30, expand=True),    # Important, Not Urgent
            ], expand=True)

            bottom_row = ft.Row(controls=[
                ft.Container(content=self._divider[1], image=ft.DecorationImage(src="icons/cont/e_blue.png",fit=ft.ImageFit.FILL), padding = 30, expand=True),  # Not Important, Urgent
                ft.Container(content=self._divider[0], image=ft.DecorationImage(src="icons/cont/e_pink.png",fit=ft.ImageFit.FILL), padding = 30, expand=True)   # Not Important, Not Urgent
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
            
    def _on_change(self,task_id,divider_index, i):
        value = self.database.change_task_completion(task_id)
        if value != None:
            self._divider[divider_index].visible = value
            self._divider[divider_index].update()
            # self.container.controls[i].visible = value
            # self.container.controls[i].update()

    def get_container(self):
        return self.container