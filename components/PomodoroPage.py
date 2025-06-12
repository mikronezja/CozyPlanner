import flet as ft 
import time
import math
import threading

class PomodoroPage:
    def __init__(self, database):
        self.main_text=ft.Text("Welcome to POMIDORO. IF READY CLICK START", size=30, weight=ft.FontWeight.BOLD, color=("#702106"))
        self.time_left=25*60
        self.running=False
        self.on_break=False
        self.break_time=5*60
        self.timer_text=ft.Text("25:00", size=50, weight=ft.FontWeight.BOLD, color=("#702106"))

        self.add_time = self._create_button("icons/pom_play_button.png", self.__add_time, reverse=True)
        self.subtract_time = self._create_button("icons/pom_play_button.png", self.__subtract_time )

        self.start_button = self._create_button("icons/pom_play_button.png", self.start_timer)
        self.pause_button = self._create_button("icons/pom_pause_button.png", self.pause_timer)
        self.stop_button = self._create_button("icons/pom_stop_button.png", self.stop_timer)
    
    def _create_button(self, icon_path, click_handler, reverse=False):
        button = ft.Container(
            content=ft.Image(src=icon_path, width=50,rotate=(math.pi if reverse else 0)),
            on_click=click_handler,
            offset=ft.Offset(0, 0)
        )
        button.on_hover = lambda e: self._handle_hover(button, e)
        return button
    
    def _handle_hover(self, button, e: ft.HoverEvent):
        button.offset = ft.Offset(0, 0.05) if e.data == "true" else ft.Offset(0, 0)
        button.update()    
    
    def __subtract_time(self,e):
        if not self.running:
            self.time_left = self.time_left - 60 if self.time_left >= 60 else 0
        if self.on_break:
            self.break_time = self.break_time - 60 if self.break_time >= 60 else 0
        self.update_timer_display()

    
    def __add_time(self,e):
        if not self.running:
            self.time_left+=60
        if self.on_break:
            self.break_time+=60
        self.update_timer_display()

    def start_timer(self,e):
        if not self.running:
            self.running=True
            self.start_button.disabled=True
            self.stop_button.disabled=False
            self.pause_button.disabled=False
            self.update_main_text()
            threading.Thread(target=self.countdown, daemon=True).start()

    def pause_timer(self,e):
        self.running=False
        self.start_button.disabled=False
        self.pause_button.disabled=True
        self.stop_button.disabled=False
        self.__update_all()

    def stop_timer(self,e):
        self.timer_text.value="25:00"
        self.timer_text.update()
        self.running=False
        self.on_break=False
        self.time_left=25*60
        self.update_main_text()
        self.start_button.disabled=False
        self.pause_button.disabled=True
        self.stop_button.disabled=True
        self.__update_all()
        
    def update_timer_display(self):
        mins,secs=divmod(self.time_left,60)
        self.timer_text.value=f"{mins:02}:{secs:02}"
        self.timer_text.update()

    def countdown(self):
        while self.running:
            if self.on_break:
                while self.time_left > 0 and self.running and self.on_break:
                    mins,secs=divmod(self.time_left,60)
                    self.timer_text.value = f"{mins:02}:{secs:02}"
                    self.timer_text.update()
                    time.sleep(1)
                    self.time_left -= 1
                if self.time_left == 0:
                    self.on_break = False
                    self.time_left = 25*60
                    self.start_timer(None)    
                    self.update_main_text()            
            else:
                while self.time_left>0 and self.running and not self.on_break:
                    mins,secs = divmod(self.time_left,60)
                    self.timer_text.value = f"{mins:02}:{secs:02}"
                    self.timer_text.update()
                    time.sleep(1)
                    self.time_left -= 1
                if self.time_left == 0:
                    self.on_break = True
                    self.time_left = self.break_time
                    self.start_timer(None)
                    self.update_main_text()
        self.update_main_text()

    def update_main_text(self):
        if self.running:
            if self.on_break:
                self.main_text.value="It's break time!! Let's get some rest.."
            else:
                self.main_text.value="Let's study! Break time in:"
        elif not self.running and self.time_left==25*60:
            self.main_text.value="Welcome to POMIDORO. IF READY CLICK START"
        self.main_text.update()

    def __update_all(self):
        self.stop_button.update()
        self.start_button.update()
        self.pause_button.update()
        self.update_main_text()

    def get_container(self):

        return ft.Container(
            # bgcolor=ft.Colors.with_opacity(0.95,("#F1E189")),
            image=ft.DecorationImage(src="icons/pomodor.png",fit=ft.ImageFit.FILL),
            margin=ft.margin.only(left=200,right=200,top=10,bottom=50),
            border_radius=ft.border_radius.all(30),
            content=ft.Column(
                [   self.main_text,
                    ft.Container(
                    content=ft.Row( controls=[self.add_time,
                                              self.timer_text, 
                                              self.subtract_time], 
                                              alignment=ft.MainAxisAlignment.CENTER),
                    alignment=ft.alignment.center),
                    ft.Row([
                    self.start_button,
                    self.pause_button,
                    self.stop_button], alignment=ft.MainAxisAlignment.CENTER)],
                
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                
            ),
            alignment=ft.alignment.center,
            expand=True
        )