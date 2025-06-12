import flet as ft 
from ..Enums.Month import Month

class SingleTask:
    def __init__(self, database, task_id, go_back):            
        self.database = database
        (task_id, date_id, name, desc, completed, urgency, importance) = self.database.get_task_with_id(task_id)

        (day,month,year) = self.__display_date(date_id)
        dates = ft.Row(controls=[ft.Text(day,size=15,color='#702106'), ft.Text(month,size=15,color='#702106'), ft.Text(year,size=15,color='#702106')])
        
        self.__back_btn = ft.Container(
                    content=ft.Image(src="../icons/go_back.png",width=200),
                    on_click=go_back,
                    offset=ft.Offset(0,0),
                    width=100,
                    on_hover=self.__on_hover
                )

        main_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(name, overflow=ft.TextOverflow.ELLIPSIS,color='#702106',size=24,max_lines=5,text_align=ft.TextAlign.CENTER),
                    width=250,
                    expand=False,
                    alignment=ft.alignment.center

                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
        desciption = ft.Container(content=ft.Text(desc,color='#702106',
                                                  size=18,
                                                  max_lines=None,
                                                  no_wrap=False,
                                                  text_align=ft.TextAlign.START,
                                                  selectable=False,
                                                  overflow=ft.TextOverflow.CLIP,)
                                                  ,padding=ft.padding.all(10),  width=250,)

        self.container = ft.Container(content=ft.Column(controls=[ft.Row(height=40),ft.Container(content=dates, width=80),main_row, desciption,self.__back_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=5), width=300)

    def __display_date(self, date_id):
        (id, day, month, year) = self.database.get_date(date_id)
        return (day, Month(month).name, year)

    def __on_hover(self, e):
        if e.data=="true":
            self.__back_btn.offset=ft.Offset(0,0.03)
        else:
            self.__back_btn.offset=ft.Offset(0,0)
        self.__back_btn.update()

    def get_container(self):
        return self.container