import flet as ft
import time
import math
import datetime
import threading
from .Sounds.Music import Music

class PomodoroPage:
    def __init__(self, database, page):
        self.running = False
        self.on_break = False
        
        self.work_duration = 25 * 60 
        self.break_duration = 5 * 60
        self.session_number = 1
        self.time_left = self.work_duration

        self.database = database

        now = datetime.datetime.now()
        self.current_day = (now.day, now.month, now.year)
        
        record = self.database.get_latest_pomodoro(*self.current_day)

        if record:
            _id, _date_id, initial_time, total_seconds, session_number, is_working = record
            self.work_duration = initial_time
            self.session_number = session_number
            self.time_left = initial_time - total_seconds
            self.on_break = not is_working

        self.main_text = ft.Text("Welcome! Click start to begin.", size=30, weight=ft.FontWeight.BOLD, color=("#702106"))
        self.timer_text = ft.Text(self.format_time(self.time_left), size=50, weight=ft.FontWeight.BOLD, color=("#702106"))

        self.add_time_button = self._create_button("icons/pom_play_button.png", self.add_time)
        self.subtract_time_button = self._create_button("icons/pom_play_button.png", self.subtract_time, reverse=True)
        
        self.start_button = self._create_button("icons/pom_play_button.png", self.start_timer)
        self.pause_button = self._create_button("icons/pom_pause_button.png", self.pause_timer)
        self.stop_button = self._create_button("icons/pom_stop_button.png", self.stop_timer)

        self.pause_button.disabled = True
        self.stop_button.disabled = True

        self.audio = Music(src='assets/music/stop.mp3',volume=1, page=page)

        self.container = self.get_container()

    def _create_button(self, icon_path, click_handler, reverse=False):
        button = ft.Container(
            content=ft.Image(src=icon_path, width=50, rotate=(math.pi if reverse else 0)),
            on_click=click_handler,
            offset=ft.Offset(0, 0)
        )
        button.on_hover = lambda e: self._handle_hover(button, e)
        return button

    def _handle_hover(self, button, e: ft.HoverEvent):
        button.offset = ft.Offset(0, 0.05) if e.data == "true" else ft.Offset(0, 0)
        if button.page:
            button.page.update()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{int(mins):02}:{int(secs):02}"

    def update_timer_display(self):
        self.timer_text.value = self.format_time(self.time_left)
        self.timer_text.update()

    def update_main_text(self):
        if self.running:
            self.main_text.value = "Time for a break!" if self.on_break else "Focus! Time to work:"
        else:
            if self.time_left < self.work_duration:
                 self.main_text.value = "Paused. Ready to continue?"
            else:
                 self.main_text.value = "Welcome! Click start to begin."
        if self.main_text.page:
            self.main_text.page.update()

    def __update_button_states(self):
        self.start_button.disabled = self.running
        self.pause_button.disabled = not self.running
        self.stop_button.disabled = not self.running and self.time_left == self.work_duration
        
        if self.start_button.page:
            self.start_button.page.update()


    def subtract_time(self, e):
        if not self.running:
            target_duration = self.break_duration if self.on_break else self.work_duration
            new_duration = max(60, ((target_duration - 60)) // 60 * 60)
            
            if self.on_break:
                self.break_duration = new_duration
            else:
                self.work_duration = new_duration
                self.time_left = self.work_duration
            
            self.update_timer_display()
            e.page.update()

    def add_time(self, e):
        if not self.running:
            target_duration = self.break_duration if self.on_break else self.work_duration
            new_duration = ((target_duration + 60) // 60) * 60
            
            if self.on_break:
                self.break_duration = new_duration
            else:
                self.work_duration = new_duration
                self.time_left = self.work_duration

            self.update_timer_display()
            e.page.update()

    def start_timer(self, e):
        if not self.running:
            self.running = True
            self.update_main_text()
            self.__update_button_states()
            threading.Thread(target=self.countdown, daemon=True).start()

    def pause_timer(self, e):
        if self.running:
            self.running = False
            self.update_main_text()
            self.__update_button_states()

    def stop_timer(self, e):
        self.running = False
        self.on_break = False
        self.time_left = self.work_duration
        self.update_timer_display()
        self.update_main_text()
        self.__update_button_states()
        
    def countdown(self):
        while self.running:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_timer_display()
                time.sleep(1)
                
                if (self.work_duration - self.time_left) % 10 == 0:
                    initial_time = self.break_duration if self.on_break else self.work_duration
                    self.database.add_pomodoro(self.current_day[0], self.current_day[1], self.current_day[2], 
                                               initial_time,initial_time - self.time_left,self.session_number,not self.on_break)
            else:
                self.database.sum_all_previous_pomodoros(*self.current_day)
                
                self.on_break = not self.on_break

                if self.on_break:
                    self.time_left = self.break_duration
                else:
                    self.time_left = self.work_duration
                self.session_number += 1

                self.audio.call()
                
                self.update_main_text()
                self.update_timer_display()

    def get_container(self):
        return ft.Container(
            image=ft.DecorationImage(src="icons/pomodor.png", fit=ft.ImageFit.FILL),
            margin=ft.margin.only(left=200, right=200, top=10, bottom=50),
            border_radius=ft.border_radius.all(30),
            content=ft.Column(
                [
                    self.main_text,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self.subtract_time_button,
                                self.timer_text, 
                                self.add_time_button
                            ], 
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Row(
                        [
                            self.start_button,
                            self.pause_button,
                            self.stop_button
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            expand=True
        )