import flet as ft 
import math

class EisenHowerPage:
    def __init__(self, tasks):
        self.tasks = tasks

        def create_container(task):
            return ft.Text(value=task.name, size = 18, color=ft.Colors.BLUE_GREY_800)

        if len(self.tasks) > 0:
            divider = [ ft.Column(spacing=10) for _ in range(4) ] 
            for task in self.tasks:
                match task.importance:
                    case 0: # Not Important, Not Urgent
                        divider[0].controls.append(create_container(task))
                    case 1: # Not Important, Urgent
                        divider[1].controls.append(create_container(task))
                    case 2: # Important, Not Urgent
                        divider[2].controls.append(create_container(task))   
                    case 3: # Important, Urgent 
                        divider[3].controls.append(create_container(task))

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