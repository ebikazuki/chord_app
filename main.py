import flet as ft
from app.models import KeySetting, ChordEvent, Progression
from app.core.theory import chord_to_asset_path, degree_to_chord
from app.core.audio import AudioEngine
from app.services.history import HistoryService
from app.services.persistence import PersistenceService
from app.services.export import ExportService
from app.ui.diatonic_grid import DiatonicGrid
from app.ui.controls import KeyModeControls, OptionPanel
from app.ui.history_bar import HistoryBar
from datetime import datetime

def main(page: ft.Page):
    page.title = "DiatonicPad MVP"
    page.window.width = 1024
    page.window.height = 600
    
    audio_engine = AudioEngine(page)
    history_service = HistoryService()
    persistence_service = PersistenceService()
    export_service = ExportService()
    
    key_setting = KeySetting(tonic="C", mode="Ionian")
    current_progression = Progression(key_setting=key_setting)
    
    def on_pad_click(degree_idx: int):
        """Handle chord pad click"""
        key_setting.tensions = option_panel.get_tensions()
        
        path = chord_to_asset_path(key_setting, degree_idx)
        audio_engine.play_sample(path)
        
        chord_spec = degree_to_chord(key_setting, degree_idx)
        event = ChordEvent(
            degree=chord_spec["degree"],
            quality=chord_spec["quality"],
            tension=key_setting.tensions.copy(),
            inversion=key_setting.inversion,
            voicing=key_setting.voicing,
        )
        history_service.push_event(event)
        current_progression.events = history_service.get_current_events()
        
        update_status()
    
    def on_key_change(new_key: str):
        key_setting.tonic = new_key
        update_status()
    
    def on_mode_change(new_mode: str):
        key_setting.mode = new_mode
        update_status()
    
    def on_tension_change():
        update_status()
    
    def on_voicing_change(new_voicing: str):
        key_setting.voicing = new_voicing
        update_status()
    
    def on_undo():
        if history_service.undo():
            current_progression.events = history_service.get_current_events()
            update_status()
    
    def on_redo():
        if history_service.redo():
            current_progression.events = history_service.get_current_events()
            update_status()
    
    def on_save():
        """Save current progression"""
        current_progression.name = f"Progression_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        current_progression.updated_at = datetime.now().isoformat()
        current_progression.key_setting = key_setting
        persistence_service.save_progression(current_progression)
        page.snack_bar = ft.SnackBar(ft.Text(f"Saved: {current_progression.name}"))
        page.snack_bar.open = True
        page.update()
    
    def on_load():
        """Load progression (simplified - loads most recent)"""
        progressions = persistence_service.list_progressions()
        if progressions:
            loaded = persistence_service.load_progression(progressions[-1]["id"])
            key_setting.tonic = loaded.key_setting.tonic
            key_setting.mode = loaded.key_setting.mode
            history_service.events = loaded.events
            history_service.current_index = len(loaded.events) - 1
            current_progression.events = loaded.events
            
            key_mode_controls.key_dropdown.value = key_setting.tonic
            key_mode_controls.mode_dropdown.value = key_setting.mode
            
            page.snack_bar = ft.SnackBar(ft.Text(f"Loaded: {loaded.name}"))
            page.snack_bar.open = True
            update_status()
    
    def on_export():
        """Export progression to WAV"""
        output_path = f"data/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        if export_service.export_wav(current_progression, output_path):
            page.snack_bar = ft.SnackBar(ft.Text(f"Exported: {output_path}"))
            page.snack_bar.open = True
            page.update()
    
    def update_status():
        """Update status text"""
        tensions_str = ", ".join(map(str, option_panel.get_tensions())) if option_panel.get_tensions() else "none"
        status_text.value = (f"Key: {key_setting.tonic} {key_setting.mode} | "
                           f"Voicing: {key_setting.voicing} | "
                           f"Tensions: {tensions_str} | "
                           f"Events: {len(current_progression.events)}")
        page.update()
    
    key_mode_controls = KeyModeControls(on_key_change, on_mode_change)
    diatonic_grid = DiatonicGrid(on_pad_click)
    option_panel = OptionPanel(on_tension_change, on_voicing_change)
    history_bar = HistoryBar(on_undo, on_redo, on_save, on_load, on_export)
    status_text = ft.Text("Ready", size=12)
    
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    key_mode_controls,
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            diatonic_grid,
                            ft.VerticalDivider(),
                            option_panel,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(),
                    history_bar,
                    status_text,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )
    
    update_status()

if __name__ == "__main__":
    ft.app(main)
