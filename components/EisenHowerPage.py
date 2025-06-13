import flet as ft 
import math
import datetime
from .Functionalities.CalendarHelpers import CalendarHelpers


class EisenHowerPage:
    def __init__(self, database, show_previous_tasks = True):
        self.database = database
        self.checkbox_refs = {}
        
        now = datetime.datetime.now()
        day, month, year = now.day, now.month, now.year
        
        tasks = self.database.get_tasks(day,month,year)

        def create_container(name, task_id, completed, divider_index,i): # for task
            self.checkbox_refs[task_id] = ft.Checkbox(fill_color = ft.Colors.PINK_100, 
                                                check_color = ft.Colors.PINK_200,
                                                value = (completed == 1),
                                                on_change = lambda e: self._on_change(task_id))

            return ft.Row(controls=[ft.Text(value=name, size = 18, color='#702106'), 
                                    self.checkbox_refs[task_id],
                                    ft.IconButton(
                                    icon=ft.Icons.CANCEL_OUTLINED,
                                    icon_color=ft.Colors.PINK_200,
                                    icon_size=23,
                                    tooltip="Remove task",
                                    on_click=lambda e: self._task_removed(task_id,divider_index,i)
                                    )
                                    ],scroll=ft.ScrollMode.AUTO, expand=True) 

        if len(tasks) > 0:
            self._divider = [ ft.Column(spacing=10,
                                        scroll=ft.ScrollMode.AUTO, # scrollowanie w poziomie
                                        expand=True,
                                        width=400,
                                        height=200,
                                        ) for _ in range(4) ] 
            if show_previous_tasks:
                prev_tasks = database.get_tasks(*CalendarHelpers.get_previous_day())
                for (task_id, date_id, name, desc, completed, urgency, importance) in prev_tasks:
                    if not completed:
                        divider_index = importance*2 + urgency
                        cont = self._divider[divider_index]
                        cont.controls.append(create_container(name,task_id,completed,divider_index, len(cont.controls)))

            for (task_id, date_id, name, desc, completed, urgency, importance) in tasks:
                divider_index = importance*2 + urgency
                cont = self._divider[divider_index]
                cont.controls.append(create_container(name,task_id,completed,divider_index, len(cont.controls)))
            

            top_labels = ft.Row([
            self._create_text("Urgent", rotate=False),
            self._create_text("Not Urgent", rotate=False)
            ])

            top_row = ft.Row(controls=[
                self._create_box(3,"icons/cont/e_yellow.png"), # Important, Urgent 
                self._create_box(2, "icons/cont/e_green.png") # important, Not Urgent
            ], expand=True)

            bottom_row = ft.Row(controls=[
                self._create_box(1,"icons/cont/e_blue.png"), # Not Important, Urgent
                self._create_box(0,"icons/cont/e_pink.png") # Not Important, Not Urgent
            ], expand=True)

            left_labels = ft.Column([
                self._create_text("Important", rotate=True),
                self._create_text("Not Important", rotate=True)
            ])

            self.container = ft.Row( [left_labels,
                                    ft.Column(controls=[top_labels,top_row,bottom_row], 
                                    expand=True)], alignment=ft.alignment.center, expand=True )
        else:
            self.container = ft.Container(
                content=ft.Text(value="No tasks have been added",color='#702106', size=25),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=50)
                )
            
    def _on_change(self,task_id):
        new_state = self.database.change_task_completion(task_id)

        if new_state is not None:
            self.checkbox_refs[task_id].value = (new_state == 1)
            self.checkbox_refs[task_id].update()
    
    def _task_removed(self,task_id, divider_index, i):
        self.database.remove_task(task_id)
        self._divider[divider_index].controls.pop(i)
        self._divider[divider_index].update()

    def _create_box(self, divider_idx, src):
        return ft.Container(content=self._divider[divider_idx], 
                            image=ft.DecorationImage(src=src,fit=ft.ImageFit.FILL),
                            width=500,
                            padding = 30, 
                            expand=True)
    
    def _create_text(self, text, rotate):
        return ft.Container(content=ft.Text(text, size=20, 
                                            weight=ft.FontWeight.BOLD,color='#702106'),
                                            expand=True, alignment=ft.alignment.center, 
                                            rotate=(ft.Rotate(angle=-math.pi/2) if rotate else ft.Rotate(angle=0)))

    def get_container(self):
        return self.container