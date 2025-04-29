import flet as ft 

SLIDER_COLOR = ft.Colors.BLACK

class InputTask:
    def __init__(self, on_input_task_click, _visible = False):
        self.name_text_field = ft.TextField( hint_text="Task name...",
                label="Task name", visible = _visible)
        self.desc_text_field = ft.TextField( hint_text="Description...",
                label="Description", visible = _visible)
        self.confirm_button = ft.ElevatedButton(text="Add", on_click=lambda _: on_input_task_click(self.name_text_field.value,
                                                                                                   self.desc_text_field.value),
                                                                                                       visible = _visible)
        self.task_importance_value = ft.Text(value="Not Important", visible=_visible)
        self.task_urgency_value = ft.Text(value="Not Urgent", visible=_visible)

        def get_cupertino_slider(change_function):
            return  ft.CupertinoSlider(
                divisions=1,
                max=1,
                min=0,
                active_color=SLIDER_COLOR,
                thumb_color=SLIDER_COLOR,
                on_change=change_function,
                visible=_visible)

        def handle_importance_change(e):
            importance_levels = {
                0:"Not Important",
                1:"Important",
            }
            self.task_importance_value.value = importance_levels.get(int(e.control.value), "Unknown")
            self.task_importance_value.update()
            self.task_importance.update()
        
        def handle_urgency_change(e):
            urgency_levels = {
                0:"Not Urgent",
                1:"Urgent",
            }
            self.task_urgency_value.value = urgency_levels.get(int(e.control.value), "Unknown")
            self.task_urgency_value.update()
            self.task_urgency.update()
        

        self.task_importance = get_cupertino_slider(handle_importance_change)
        self.task_urgency = get_cupertino_slider(handle_urgency_change)


        self.container = ft.Container(
            ft.Column(
                controls=[self.name_text_field, 
                          self.desc_text_field, 
                          self.task_importance_value,
                          self.task_importance, 
                          self.task_urgency_value,
                          self.task_urgency,
                          self.confirm_button]
            ),
            alignment=ft.alignment.center
        )

    def set_visible(self, value):
        self.name_text_field.visible = value
        self.desc_text_field.visible = value
        self.confirm_button.visible = value
        self.task_importance.visible = value
        self.task_importance_value.visible = value
        self.task_urgency.visible = value
        self.task_urgency_value.visible = value
 
    def reset_field_values(self):
        self.name_text_field.value = "Task name..."
        self.desc_text_field.value = "Description..."

    def update(self):
        self.container.update()

    def get_container(self): 
        return self.container