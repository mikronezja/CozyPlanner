import flet as ft 

class InputTask:
    def __init__(self, on_input_task_click, _visible = False):
        self.name_text_field = ft.TextField( hint_text="Task name...",
                label="Task name", visible = _visible)
        self.desc_text_field = ft.TextField( hint_text="Description...",
                label="Description", visible = _visible)
        self.confirm_button = ft.ElevatedButton(text="Add", on_click=lambda _: on_input_task_click(self.name_text_field.value,
                                                                                                   self.desc_text_field.value),
                                                                                                   visible = _visible)
        self.container = ft.Container(
            ft.Column(
                controls=[self.name_text_field, self.desc_text_field, self.confirm_button]
            ),
            alignment=ft.alignment.center
        )

    def set_visible(self, value):
        self.name_text_field.visible = value
        self.desc_text_field.visible = value
        self.confirm_button.visible = value
 
    def reset_field_values(self):
        self.name_text_field.value = "Task name..."
        self.desc_text_field.value = "Description..."


    def update(self):
        self.container.update()

    def get_container(self): 
        return self.container