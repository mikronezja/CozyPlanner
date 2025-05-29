import flet as ft 

SLIDER_COLOR = ft.Colors.BLACK
confirm_button_src = "icons/add_task_button.png"

class InputTask:
    def __init__(self, on_input_task_click, _visible = False):
        self.name_text_field = ft.TextField( hint_text="Task name...",
                label="Task name", visible = _visible,color=ft.Colors.BLACK,width=200)
        self.desc_text_field = ft.TextField( hint_text="Description...",
                label="Description", visible = _visible,color=ft.Colors.BLACK,width=200)
        # self.confirm_button = ft.ElevatedButton(text="Add", on_click=lambda _: on_input_task_click(self.name_text_field.value,
        #                                                                                            self.desc_text_field.value),
        #                                                                                                visible = _visible)

        self.confirm_button=ft.Container(
            content=ft.Image(src=confirm_button_src,width=150),
            on_click=lambda _: on_input_task_click(self.name_text_field.value,self.desc_text_field.value),
            on_hover=self._on_confirm_hover,
            offset=ft.Offset(0,0),
            visible=_visible
        )

        self.task_importance_value = ft.Text(value="Not Important", visible=_visible,color=ft.Colors.BLACK)
        self.task_urgency_value = ft.Text(value="Not Urgent", visible=_visible,color=ft.Colors.BLACK)

        def get_cupertino_slider(change_function):
            return  ft.CupertinoSlider(
                divisions=1,
                max=1,
                min=0,
                active_color=SLIDER_COLOR,
                thumb_color=SLIDER_COLOR,
                on_change=change_function,
                visible=_visible)
        def get_slider(change_function):
            slider= ft.Slider(
                min=0,
                max=1,
                divisions=1,
                value=0,
                active_color=ft.Colors.YELLOW_400,
                inactive_color=ft.Colors.PINK_100,
                thumb_color=ft.Colors.PINK_200,
                on_change=change_function,
                visible=_visible
            )
            container= ft.Container(
                slider,
                width=200,  
                alignment=ft.alignment.center
            )
            return slider,container
        def handle_importance_change(e):
            importance_levels = {
                0:"Not Important",
                1:"Important",
            }
            self.task_importance_value.value = importance_levels.get(int(e.control.value), "Unknown")
            self.task_importance_value.update()
            self.task_importance_slider.value = e.control.value
            self.task_importance_slider.update()
        
        def handle_urgency_change(e):
            urgency_levels = {
                0:"Not Urgent",
                1:"Urgent",
            }
            self.task_urgency_value.value = urgency_levels.get(int(e.control.value), "Unknown")
            self.task_urgency_value.update()
            self.task_urgency_slider.value = e.control.value
            self.task_urgency_slider.update()
        

        # self.task_importance = get_cupertino_slider(handle_importance_change)
        # self.task_urgency = get_cupertino_slider(handle_urgency_change)
        self.task_importance_slider,self.task_importance = get_slider(handle_importance_change)
        self.task_urgency_slider,self.task_urgency = get_slider(handle_urgency_change)


        # self.container = ft.Container(
        #     ft.Column(
        #         controls=[self.name_text_field, 
        #                   self.desc_text_field, 
        #                   self.task_importance_value,
        #                   self.task_importance, 
        #                   self.task_urgency_value,
        #                   self.task_urgency,
        #                   self.confirm_button]
        #     ),
        #     alignment=ft.alignment.center
        # )
        self.container = ft.Container(
            visible =_visible,
            content = ft.Container(
                content = ft.Column(
                    controls=[
                        self.name_text_field,
                        self.desc_text_field,
                        self.task_importance_value,
                        self.task_importance,
                        self.task_urgency_value,
                        self.task_urgency,
                        self.confirm_button
                    ],
                    alignment = ft.MainAxisAlignment.START,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                ),
                #padding=ft.padding.all(20),
                padding = ft.padding.only(left=30, right=30, top=50, bottom=50),
                width = 400,
                height = 500,
                alignment=ft.alignment.top_center
            ),
            width = 400,
            height = 500,
            border_radius = 5,
            image = ft.DecorationImage(
                src = "icons/list.png", 
                fit = ft.ImageFit.FILL,
                repeat = ft.ImageRepeat.NO_REPEAT,
                alignment = ft.alignment.center
            )
        )


    def set_visible(self, value):
        self.container.visible=value
        self.name_text_field.visible = value
        self.desc_text_field.visible = value
        self.confirm_button.visible = value
        self.task_importance.visible = value
        self.task_importance_value.visible = value
        self.task_urgency.visible = value
        self.task_urgency_value.visible = value
        self.task_importance_slider.visible = value
        self.task_urgency_slider.visible = value

    def _on_confirm_hover(self, e: ft.HoverEvent):
        if e.data == "true":
            self.confirm_button.offset = ft.Offset(0, 0.03)
        else:
            self.confirm_button.offset = ft.Offset(0, 0)
        self.confirm_button.update()

    def reset_field_values(self):
        self.name_text_field.value = "Task name..."
        self.desc_text_field.value = "Description..."

    def update(self):
        self.container.update()

    def get_container(self): 
        return self.container