import flet as ft
import datetime



# today
## number of tasks,
## number of tasks completed,
## minutes in pomodoro
## pomodoro sessions
## mood score


# + add total and average
# month 

# year


class StatisticsPage:
    def __init__(self, database):
        self.database = database
        now = datetime.datetime.now()
        self.current_day = (now.day, now.month, now.year)
        self.current_day

        self.current_statistics = 'day'

        self.month_button = ft.ElevatedButton(text="month")
        self.day_button = ft.ElevatedButton(text="day", visible=False)
        self.year_button = ft.ElevatedButton(text="year")

        ## button -> year
        ## button -> monthly 

    def current_statistics_container(self):
        number_of_tasks = ft.Text(value="Number of todays tasks : " )
        number_of_tasks_completed = ft.Text(value="Number of todays tasks : ")
        minutes_in_pomodoro = ft.Text(value = "Minutes in pomodoro : ")
        sessions_in_pomodoro = ft.Text(value = "Sessions in pomodoro : ")

        if self.current_statistics == 'day':
            ## number of tasks,
            todays_tasks = self.database.get_tasks(*self.current_day)
            number_of_tasks.value += str(len(todays_tasks))

            ## number of tasks completed,
            completed_task_counter = 0
            for (task_id, date_id, name, desc, completed, urgency, importance) in todays_tasks:
                if completed:
                    completed_task_counter+=1
            
            number_of_tasks_completed.value += str(completed_task_counter)
            ## minutes in pomodoro
            day_pomodoros = self.database.get_pomodoros_from_day(*self.current_day)

            minute_count = 0
            pom_count = 0
            for (_,_,_,total_seconds,_,is_working) in day_pomodoros:
                if is_working:
                    pom_count += 1
                    minute_count = total_seconds

            minutes_in_pomodoro.value += str(minute_count)
            ## pomodoro sessions
            sessions_in_pomodoro.value += str(pom_count)
            ## mood score
            journal = self.database.get_journal(*self.current_day)
            mood_score = ft.Text(value="Mood score : " + str(journal.mood_score)) if journal else ft.Text("No journal was written")
            return ft.Container(
                content=ft.Column(controls=[
                    ft.Row(controls=[number_of_tasks, number_of_tasks_completed]),
                    ft.Row(controls=[minutes_in_pomodoro,sessions_in_pomodoro]),
                    ft.Row(controls=[mood_score])
                ])
                )
        elif self.current_statistics == 'month':
            pass
        elif self.current_statistics == 'year':
            pass
        else:
            pass

    def get_container(self):
        return ft.Container(content=ft.Row(controls=[
            self.month_button,
            self.current_statistics_container(),
            self.day_button,
            self.year_button,
        ]) )
    