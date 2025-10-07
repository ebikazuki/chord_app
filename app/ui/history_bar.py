import flet as ft
from typing import Callable

class HistoryBar(ft.Container):
    """Transport controls and history management"""
    
    def __init__(self, on_undo: Callable, on_redo: Callable,
                 on_save: Callable, on_load: Callable, on_export: Callable):
        super().__init__()
        
        self.content = ft.Row(
            controls=[
                ft.ElevatedButton("Undo", icon=ft.Icons.UNDO, on_click=lambda e: on_undo()),
                ft.ElevatedButton("Redo", icon=ft.Icons.REDO, on_click=lambda e: on_redo()),
                ft.VerticalDivider(),
                ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=lambda e: on_save()),
                ft.ElevatedButton("Load", icon=ft.Icons.FOLDER_OPEN, on_click=lambda e: on_load()),
                ft.ElevatedButton("Export", icon=ft.Icons.DOWNLOAD, on_click=lambda e: on_export()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
