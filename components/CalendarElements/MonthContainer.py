import flet as ft
import calendar
from .DateBox import DayContainer
from ..Enums.WeekDay import WeekDay

class MonthContainer:
    def __init__(self,database, month, year, higher_on_click, show_nav_callback=None):
        self.database = database
        self.month = month
        self.year = year
        self.higher_on_click = higher_on_click
        self.show_nav_callback = show_nav_callback
        self.month_days = calendar.monthrange(year, month)[1]
        self.starting_weekday = calendar.monthrange(year, month)[0]
        self.days_container = [ DayContainer(day=i,month=month, year=year, 
                                             on_click=lambda e, 
                                             day=i: self.__on_click(e,day,month,year,higher_on_click)) for i in range(1, self.month_days+1) ]

        self.default_container = self.__create_month_view()
        

        self.container = ft.Container(
            content=self.default_container,
            width=714,
        )

    def __create_month_view(self):
        month_view = ft.Column(
            spacing=2,
            width=714
        )
        
        header_row = ft.Row(
            spacing=2, 
            alignment=ft.MainAxisAlignment.START
        )
        
        for i in range(len(WeekDay)):
            header_container = ft.Container(
                content=ft.Text(
                    WeekDay(i).name,
                    size=16, 
                    color='#702106',
                    weight=ft.FontWeight.BOLD
                ),
                width=100,
                height=30,
                alignment=ft.alignment.center,
                border_radius=3
            )
            header_row.controls.append(header_container)

        month_view.controls.append(header_row)

        row = ft.Row(
            spacing=2,
            alignment=ft.MainAxisAlignment.START
        )
        
        # jesli sie nie zaczyna od poniedzialku
        for _ in range(self.starting_weekday):
            empty_container = ft.Container(
                width=100,
                height=50 
            )
            row.controls.append(empty_container)

        for day in self.days_container:
            if len(row.controls) == 7:
                month_view.controls.append(row)
                row = ft.Row(
                    spacing=2,
                    alignment=ft.MainAxisAlignment.START
                )
            row.controls.append(day)

        # Add the last row if it has any controls
        while len(row.controls) != 7:
            row.controls.append(ft.Container(
                width=100,
                height=50 
            ))
        month_view.controls.append(row)      
        
        return month_view
    
    def _handle_hover(self, button, e: ft.HoverEvent):
        button.offset = ft.Offset(0, 0.05) if e.data == "true" else ft.Offset(0, 0)
        if button.page:
            button.page.update()

    def __on_click(self,e,day,month,year,higher_on_click):
        higher_on_click(e)
        day_view = self.__day_container(day,month,year)
        self.container.content = day_view
        self.container.update()
    
    def __day_container(self,day,month,year): 
        values = self.database.get_journal(day,month,year)

        # default values
        description = ft.TextField(value="Your journal...",color='#702106',bgcolor=ft.Colors.WHITE,border_color='#702106', multiline=True, min_lines=3, max_lines=6)
        mood_score = ft.Slider(                
                min=0,
                max=4,
                divisions=4,
                value=2,  # Default value
                active_color=ft.Colors.YELLOW_400,
                inactive_color=ft.Colors.PINK_100,
                thumb_color=ft.Colors.PINK_200,
                )
        
        if values:
            (id, date_id, journal, md_score) = values
            description.value = journal
            mood_score.value = md_score
        
        def save_journal(e):
            journal_text = description.value
            mood_value = int(mood_score.value)
            
            # Check if journal entry exists
            existing_values = self.database.get_journal(day, month, year)
            
            if existing_values:
                self.database.change_journal(day, month, year, journal_text, mood_value)
            else:
                self.database.add_journal(day, month, year, journal_text, mood_value)

        def go_back(e):
            self.container.content = self.default_container
            if self.show_nav_callback:
                self.show_nav_callback()
            self.container.update()
        
        confirm_button = ft.Container(
            content=ft.Text(),
            width=100,
            height=50,
            image=ft.DecorationImage(src='icons/save_btn.png', 
                                     fit=ft.ImageFit.FILL),
            on_click=save_journal,
            on_hover=lambda e: self._handle_hover(confirm_button,e)
        )

        back_button=ft.Container(
            content=ft.Text(),
            width=100,
            height=50,
            image=ft.DecorationImage(src='icons/back_to_calendar.png', 
                                     fit=ft.ImageFit.FILL),
            on_click=go_back,
            on_hover=lambda e: self._handle_hover(back_button,e)
        )

        def mood_container(src):
            return ft.Container(content=ft.Text(), 
                                width=100,height=50, 
                                image=ft.DecorationImage(src=src, fit=ft.ImageFit.FILL))
        
        moods_srcs = [
            'icons/mood_icons/crying_face.png',
            'icons/mood_icons/sad_face.png',
            'icons/mood_icons/mid_face.png',
            'icons/mood_icons/happy_face.png',
            'icons/mood_icons/heart_face.png'
        ]

        mood_labels = ft.Row(controls=[], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        for src in moods_srcs:
            mood_labels.controls.append(mood_container(src))
        
        return ft.Column(
            controls=[
                back_button,
                ft.Text(f"Journal for {day}/{month}/{year}",color='#702106',size=20, weight=ft.FontWeight.BOLD),
                description, 
                ft.Text("Mood Score:", size=16,color='#702106', weight=ft.FontWeight.BOLD),
                mood_labels,
                mood_score,
                ft.Row(
                    controls=[confirm_button], 
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
    

    def get_container(self):
        return self.container