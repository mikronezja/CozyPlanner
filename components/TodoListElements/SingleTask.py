import flet as ft 

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
                # ft.Container(content=dates, width=80),
                ft.Container(
                    content=ft.Text(name, overflow=ft.TextOverflow.ELLIPSIS,color='#702106',size=24,max_lines=5,text_align=ft.TextAlign.CENTER),
                    width=250,
                    expand=False,
                    alignment=ft.alignment.center

                ),
                # self.__back_btn
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )

<<<<<<< HEAD
        # desciption = ft.Row(controls=[ft.Text(desc,color='#702106',size=18,max_lines=None,no_wrap=False,text_align=ft.TextAlign.START)],width=200)
        desciption = ft.Container(content=ft.Text(desc,color='#702106',size=18,max_lines=None,no_wrap=False,text_align=ft.TextAlign.START,selectable=False,overflow=ft.TextOverflow.CLIP,),padding=ft.padding.all(10),  width=250,)

        self.container = ft.Container(content=ft.Column(controls=[ft.Row(height=40),ft.Container(content=dates, width=80),main_row, desciption,self.__back_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=5), width=300)
=======
        desciption = ft.Row(controls=[ft.Text(desc,color='#702106',size=18,max_lines=None,width=250,no_wrap=False,text_align=ft.TextAlign.START)],width=200)
        self.container = ft.Container(content=ft.Column(controls=[ft.Row(height=40),ft.Container(content=dates, width=80),main_row, desciption,self.__back_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5), width=300)
>>>>>>> 44bd27c2b7768f49bc116a97eea8a5c9ccb4c091

    def __display_date(self, date_id):
        month_class = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "June",
            7: "July",
            8: "Aug",
            9: "Sept",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }
        (id, day, month, year) = self.database.get_date(date_id)
        return (day, month_class[month], year)

    def __on_hover(self, e):
        if e.data=="true":
            self.__back_btn.offset=ft.Offset(0,0.03)
        else:
            self.__back_btn.offset=ft.Offset(0,0)
        self.__back_btn.update()

    def get_container(self):
        return self.container