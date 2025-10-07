import flet as ft
from typing import Callable
from app.core.theory import KEYS, MODES

class KeyModeControls(ft.Container):
    """Key and mode selection controls"""
    
    def __init__(self, on_key_change: Callable, on_mode_change: Callable):
        super().__init__()
        
        self.key_dropdown = ft.Dropdown(
            label="Key",
            options=[ft.dropdown.Option(key) for key in KEYS],
            value="C",
            on_change=lambda e: on_key_change(e.control.value),
        )
        
        self.mode_dropdown = ft.Dropdown(
            label="Mode",
            options=[ft.dropdown.Option(mode) for mode in MODES],
            value="Ionian",
            on_change=lambda e: on_mode_change(e.control.value),
        )
        
        self.content = ft.Row(
            controls=[self.key_dropdown, self.mode_dropdown],
            spacing=10,
        )

class OptionPanel(ft.Container):
    """Tension, inversion, voicing controls"""
    
    def __init__(self, on_tension_change: Callable, on_voicing_change: Callable):
        super().__init__()
        
        self.tension_7 = ft.Checkbox(label="7th", value=False, 
                                     on_change=lambda e: on_tension_change())
        self.tension_9 = ft.Checkbox(label="9th", value=False,
                                     on_change=lambda e: on_tension_change())
        
        self.voicing_dropdown = ft.Dropdown(
            label="Voicing",
            options=[
                ft.dropdown.Option("closed"),
                ft.dropdown.Option("drop2"),
                ft.dropdown.Option("root_shell"),
            ],
            value="drop2",
            on_change=lambda e: on_voicing_change(e.control.value),
        )
        
        self.content = ft.Column(
            controls=[
                ft.Text("Tensions", weight=ft.FontWeight.BOLD),
                self.tension_7,
                self.tension_9,
                self.voicing_dropdown,
            ],
            spacing=5,
        )
    
    def get_tensions(self):
        """Get selected tensions"""
        tensions = []
        if self.tension_7.value:
            tensions.append(7)
        if self.tension_9.value:
            tensions.append(9)
        return tensions
