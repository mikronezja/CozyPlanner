import flet as ft
import datetime
from .Enums.WeekDay import WeekDay


# today
## number of tasks,
## number of tasks completed,
## minutes in pomodoro
## pomodoro sessions
## mood score


# + add total and average
# month 

# year

TEXT_COLOR='#702106'
class StatisticsPage:
    def __init__(self, database):
        self.database = database
        now = datetime.datetime.now()
        self.current_day = (now.day, now.month, now.year)
        self.current_statistics = 'day'

        self.month_button = ft.ElevatedButton(text="month")
        self.day_button = ft.ElevatedButton(text="day")
        self.year_button = ft.ElevatedButton(text="year")
        self.week_button=ft.ElevatedButton(text="week", on_click=self.week_on_click,visible=True)
        self.stats_task=ft.Container(
            content=self.stat_chart(),
            visible=False,
            expand=True)
        ## button -> year
        ## button -> monthly 
    def week_on_click(self,e):
        self.stats_task.visible=True
        self.stats_task.content=self.stat_chart()
        self.stats_task.update()
        self.week_button.visible=False
        self.week_button.update()
        
    def current_statistics_container(self):
        number_of_tasks = ft.Text(value="Today you commited to ", color=TEXT_COLOR ,size=20)
        # number_of_tasks_completed = ft.Text(value="and completed ", color=TEXT_COLOR)
        minutes_in_pomodoro = ft.Text(value = "You spent a total of ",color=TEXT_COLOR,size=20)
        # sessions_in_pomodoro = ft.Text(value = "in a whole ",color=TEXT_COLOR)

        if self.current_statistics == 'day':
            ## number of tasks,
            todays_tasks = self.database.get_tasks(*self.current_day)
            number_of_tasks.value += str(len(todays_tasks))

            ## number of tasks completed,
            completed_task_counter = 0
            for (task_id, date_id, name, desc, completed, urgency, importance) in todays_tasks:
                if completed:
                    completed_task_counter+=1
            number_of_tasks.value+=" tasks and completed "
            number_of_tasks.value += str(completed_task_counter)
            number_of_tasks.value+=" of them!!!"
            ## minutes in pomodoro
            day_pomodoros = self.database.get_pomodoros_from_day(*self.current_day)

            minute_count = 0
            pom_count = 0
            for (_,_,_,total_seconds,_,is_working) in day_pomodoros:
                if is_working:
                    pom_count += 1
                    minute_count = total_seconds

            minutes_in_pomodoro.value += str(minute_count)
            minutes_in_pomodoro.value += " minutes in pomodoro in a whole "
            ## pomodoro sessions
            minutes_in_pomodoro.value += str(pom_count)
            minutes_in_pomodoro.value+=" sessions."
            ## mood score
            journal = self.database.get_journal(*self.current_day)
            mood_score = ft.Text(value="Your today's mood was : " + str(journal.mood_score), color=TEXT_COLOR,size=20) if journal else ft.Text("No journal was written today!", color=TEXT_COLOR,size=20)
            ending_text=ft.Text(value="Thank you for today's work! See you again tomorrow!!", color=TEXT_COLOR,size=20)
            # ending_text="Thank you for today's work! See you again tomorrow!!"
            if completed_task_counter>0:
                ending_text.value="What a valuable day! Keep up the good work!!"
            return ft.Container(
                content=ft.Column(controls=[
                    ft.Row(controls=[number_of_tasks]),
                    ft.Row(controls=[minutes_in_pomodoro]),
                    ft.Row(controls=[mood_score]),
                    ft.Row(controls=[ending_text])
                ],
                alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=20
                )
        # elif self.current_statistics == 'week':
        #     pass
        # elif self.current_statistics == 'year':
        #     pass
        else:
            pass
    
    def exit_on_click(self, e):
        self.stats_task.visible = False
        self.week_button.visible = True
        self.stats_task.update()
        self.week_button.update()
    def stat_chart(self):
        exit_button=ft.ElevatedButton(text="exit", on_click=self.exit_on_click,visible=True)
        
        title=ft.Container(
            content=ft.Text(
                value="Here's your weekly productivity chart - tasks!!", color=TEXT_COLOR, size=15
            ),
            alignment=ft.alignment.center
        )
        data=self.database.get_completed_task_from_last_week()
        # print(data)
        day_order=list(WeekDay)
        bar_chart=ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=weekday.value,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            # to_y=data.get(weekday.name,0),
                            to_y=data[weekday][1],
                            width=20,
                            color=ft.Colors.PINK_100,
                            border_radius=0,
                            rod_stack_items=[
                                ft.BarChartRodStackItem(
                                    from_y=0,
                                    to_y=data[weekday][0],
                                    color=ft.Colors.YELLOW_400
                                )
                            ]
                        )
                    ]
                )
                for weekday in WeekDay
            ],
            height=200,
            width=500,
            # alignment=ft.alignment.center
        )
        labels = ft.Row(
        controls=[
            ft.Text(weekday.name, width=50, text_align="center", color=TEXT_COLOR)
            for weekday in WeekDay
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
        return ft.Column(
            controls=[title,bar_chart,labels, exit_button]
        )

    def get_container(self):
        return ft.Container(content=ft.Row(controls=[
            # self.month_button,
            self.current_statistics_container(),
            # self.day_button,
            # self.year_button,
            self.week_button,
            self.stats_task
        ],
        alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center )
    