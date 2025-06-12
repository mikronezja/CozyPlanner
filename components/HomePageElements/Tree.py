import flet as ft
import asyncio
class Tree:
    def __init__(self):
        self.tree_image = ft.Image(
            src="icons/tree.png",
            height=500
        )
        self.tree_container = ft.Container(
            content=self.tree_image,
            on_click=self.on_tree_click,
            on_hover=self._on_hover,
            scale=1.0,
            animate_scale=ft.Animation(20),
            width=500,
            height=500,
            alignment=ft.alignment.center
        )
        # self.tree =ft.Container(
        #     content=ft.Image(
        #         src="icons/tree.png",
        #         height=500,
        #     ),
        #     on_click=self.on_tree_click,
        #     on_hover=self._on_hover,
        #     scale=1.0,
        #     animate_offset=300,
        #     animate_scale=ft.Animation(300)
        # )
        self.frog_image = ft.Image(src="icons/frog.png", height=100)
        self.frog = ft.Container(
        content=self.frog_image,
        padding=ft.Padding(top=290, left=0, right=0, bottom=0),
        visible=False,
        on_hover=self.on_frog_hover,
        offset=ft.Offset(0,0)
       )
        self.frog.animate_offset = ft.Animation(500)

        self.container = ft.Stack(
            controls=[
                self.tree_container,
                self.frog
            ],
            width=500,
            height=500,
        )
        # self.tree.on_click = self.on_tree_click
        # self.tree.on_hover=self._on_hover

    def on_tree_click(self, e):
        self.frog.visible = not self.frog.visible
        self.frog.update()
    def on_frog_hover(self,e: ft.HoverEvent):
        if e.data=="true":
            self.frog.offset=ft.Offset(0,-0.5)
            self.frog.update()
        else:
            self.frog.offset=ft.Offset(0,0)
        self.frog.update()
    
    def _on_hover(self, e: ft.HoverEvent):
        if e.data=="true":
            self.tree_container.scale=1.001
        else:
            self.tree_container.scale=1.0
        self.tree_container.update()
    def get_container(self):
        return self.container
