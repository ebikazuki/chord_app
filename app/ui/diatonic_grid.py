import flet as ft
from typing import Callable
from app.core.theory import DEGREE_NAMES

class DiatonicGrid(ft.Container):
    """Main chord pad grid with 7 diatonic degrees"""
    
    def __init__(self, on_pad_click: Callable[[int], None]):
        super().__init__()
        self.on_pad_click = on_pad_click
        
        pads = []
        for i, degree in enumerate(DEGREE_NAMES):
            pad = ft.ElevatedButton(
                text=degree,
                width=100,
                height=100,
                on_click=lambda e, idx=i: self.on_pad_click(idx),
            )
            pads.append(pad)
        
        self.content = ft.Row(
            controls=pads,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
