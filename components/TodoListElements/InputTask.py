import flet as ft 

class InputTask(ft.Container):
    def __init__(self, on_input_task_click):
        self.name_text_field = ft.TextField( value="Task name...",
                label="Task name")
        self.desc_text_field = ft.TextField( value="Description...",
                label="Description")
        self.confirm_button = ft.ElevatedButton(text="Add", on_click=lambda _: on_input_task_click(self.name_text_field,
                                                                                                   self.desc_text_field.value))
        self.container = ft.Container(
            ft.Column(
                controls=[self.name_text_field, self.desc_text_field, self.confirm_button]
            ),
            alignment=ft.alignment.center
        )

    def update(self):
        return super().update()

    def get_container(self): 
        return self.container