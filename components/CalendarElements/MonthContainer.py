import flet as ft
import calendar
from .DateBox import DayContainer
from ..Enums.WeekDay import WeekDay

WEEK_DAY_SIZE = 7

class MonthContainer:
    def __init__(self,database, month, year, higher_on_click, show_nav_callback=None):
        self.database = database
        self.month = month
        self.year = year
        self.higher_on_click = higher_on_click
        self.show_nav_callback = show_nav_callback
        self.month_days = calendar.monthrange(year, month)[1]
        self.starting_weekday = calendar.monthrange(year, month)[0]
        self.days_container = [ DayContainer(day=i,month=month, year=year, on_click=lambda e, day=i: self.__on_click(e,day,month,year,higher_on_click)) for i in range(1, self.month_days+1) ]

        ## self.container
        self.default_container = self.__create_month_view()
        
        self.container = ft.Container(
            content=self.default_container,
            expand=True
        )

    def __create_month_view(self):
        month_view = ft.Column()
        
        header_row = ft.Row()
        for i in range(WEEK_DAY_SIZE):
            header_row.controls.append(ft.Container(content=ft.Text(WeekDay(i).name,size=30, color=ft.Colors.BLUE_GREY_800),width=100, height=50,alignment=ft.alignment.center))

        month_view.controls.append(header_row)

        row = ft.Row()
        # dodaje puste pola do poczatku tygodnia
        for _ in range(self.starting_weekday):
            row.controls.append(ft.Container(width=100,height=50))

        for day in self.days_container:
            if len(row.controls) == 7:
                month_view.controls.append(row)
                row = ft.Row()
            row.controls.append(day)

        if row.controls:
            month_view.controls.append(row)
        
        return month_view

    def __on_click(self,e,day,month,year,higher_on_click):
        higher_on_click(e)
        day_view = self.__day_container(day,month,year)
        self.container.content = day_view
        self.container.update()
    
    def __day_container(self,day,month,year): 
        values = self.database.get_journal(day,month,year)

        # default values
        description = ft.TextField(value="Your journal...", multiline=True, min_lines=3, max_lines=6)
        mood_score = ft.Slider(                
                min=0,
                max=4,
                divisions=4,
                value=2,  # Default value
                active_color=ft.Colors.YELLOW_400,
                inactive_color=ft.Colors.PINK_100,
                thumb_color=ft.Colors.PINK_200,
                )
        
        if values: # values != None
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
        
        confirm_button = ft.Button(
            text='Save',
            on_click=save_journal
        )

        back_button = ft.Button(
            text='← Back to Calendar',
            on_click=go_back
        )

        # Add mood score labels
        mood_labels = ft.Row([
            ft.Text("😢", size=16),
            ft.Text("😐", size=16),
            ft.Text("🙂", size=16),
            ft.Text("😊", size=16),
            ft.Text("😄", size=16),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        return ft.Column(
            controls=[
                back_button,
                ft.Text(f"Journal for {day}/{month}/{year}", size=20, weight=ft.FontWeight.BOLD),
                description, 
                ft.Text("Mood Score:", size=16),
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