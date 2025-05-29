import flet as ft 

BGCOLOR = "white"
BORDER_RADIUS = 5
MARGIN = 5

class TaskDisplay: # tasks being displayed
    def __init__(self, database, todays_date, on_task_click):
        # self.tasks = tasks

        self.database = database
        self.todays_date = (todays_date.day, todays_date.month, todays_date.year)
        self.on_task_clicked = on_task_click

        self.task_container = []
        self.task_column = ft.Column(spacing=8)

        for i, (task_id, date_id, name, desc, completed, urgency, importance) in enumerate(database.get_tasks(*self.todays_date)):
            self._add_checkbox_removebutton(name,task_id,id=i)
        # end for

        self.container = ft.Container(content=self.task_column, 
                                      border_radius=BORDER_RADIUS,
                                      alignment=ft.alignment.top_center,
                                      padding=ft.padding.only(left=0, right=30, top=0, bottom=30),
                                      #alignment=ft.alignment.center,
                                      #margin=MARGIN,
                                      height=600,
                                      width=400,
                                      bgcolor=ft.Colors.TRANSPARENT,
                                      #image=ft.DecorationImage(src="icons/list.png",fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT,alignment=ft.alignment.center)
                                      
                                      )
    
    def task_append(self, name, idx_in_database):
        next_index = len(self.task_container)
        self._add_checkbox_removebutton(name,idx_in_database,next_index)
        self.task_column.update()

    def _add_checkbox_removebutton(self,name,task_id,id):
        text_container = ft.Container(
            content=ft.Text(
                name,
                overflow=ft.TextOverflow.ELLIPSIS, # pokazuje ... dla dlugich tekstow
                max_lines=2,
                size=18,
                weight=ft.FontWeight.NORMAL,
                color='#702106'
            ),
            width=150,
            height=50,
            padding=ft.padding.all(1),
            alignment=ft.alignment.center_left
        )
        check_box = ft.Checkbox(check_color=ft.Colors.PINK_300,
                    fill_color = ft.Colors.PINK_100,
                    hover_color=ft.Colors.PINK_100,
                    active_color=ft.Colors.PINK_200,
                    value = 0, 
                    on_change=lambda e: self.on_change(task_id, id),
                    label_position = ft.LabelPosition.LEFT)
        
        remove_button = ft.IconButton(
                    icon = ft.Icons.CANCEL_OUTLINED,
                    icon_color = ft.Colors.PINK_300,
                    icon_size = 23,
                    tooltip = "Remove task",
                    on_click = lambda e: self._task_removed(task_id, id)
                )
        display_btn = ft.Container(
            content=ft.Image(src="../icons/more.png"),
            width=50,
            # height=80,
            on_click=lambda e: self.on_task_clicked(task_id)
        )
        
        buttons_row=ft.Container(
            content=ft.Row(
                controls=[
                    check_box,
                    remove_button,
                    display_btn
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment
            )
        )
        task_row = ft.Container(
            content=ft.Row(
                controls=[
                    text_container,
                    # check_box, 
                    # remove_button, 
                    # display_btn
                    buttons_row
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            width=400,
            height=60,
            padding=ft.padding.all(1),
            margin=ft.margin.symmetric(vertical=2)
        )
        self.task_container.append(task_row)
        self.task_column.controls.append(task_row)

    def on_change(self, id, i):
        self.database.change_task_completion(id)
        self.task_container[i].update()

    def _task_removed(self,task_id, i):
        self.database.remove_task(task_id)
        self.task_container[i].visible = False
        self.task_container[i].update()

    def set_visible(self, value):
        self.container.visible = value

    def get_container(self):
        return self.container