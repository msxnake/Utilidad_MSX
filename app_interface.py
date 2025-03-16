# app_interface.py
# Programa utilidad MSX versión 0006 - Interfaz gráfica

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import os
from process_tga import process_sprites_atlas


class MainApp(MDApp):
    def build(self):
        self.title = "Utilidad MSX"
        self.fila = "1"
        self.columna = "1"
        self.num_sprites = "1"
        self.color_fondo = "255,255,255"  # Blanco como valor por defecto

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        title_label = MDLabel(
            text="Utilidad MSX",
            halign="center",
            theme_text_color="Primary",
            font_style="H5"
        )
        layout.add_widget(title_label)

        # Entradas para los parámetros
        self.fila_input = MDTextField(
            hint_text="Fila (por defecto 1)",
            text=self.fila,
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.fila_input)

        self.columna_input = MDTextField(
            hint_text="Columna (por defecto 1)",
            text=self.columna,
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.columna_input)

        self.num_sprites_input = MDTextField(
            hint_text="Número de Sprites (por defecto 1)",
            text=self.num_sprites,
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.num_sprites_input)

        self.color_fondo_input = MDTextField(
            hint_text="Color de Fondo (por defecto 255,255,255)",
            text=self.color_fondo,
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.color_fondo_input)

        # Botones
        load_button = MDRaisedButton(
            text="Load TGA",
            pos_hint={"center_x": 0.5},
            on_release=self.open_file_chooser
        )
        layout.add_widget(load_button)

        exit_button = MDRaisedButton(
            text="Salir",
            pos_hint={"center_x": 0.5},
            on_release=self.stop_app
        )
        layout.add_widget(exit_button)

        return layout

    def open_file_chooser(self, instance):
        file_chooser = FileChooserListView(filters=["*.tga"], path=os.getcwd())
        popup = Popup(
            title="Seleccionar archivo TGA",
            content=file_chooser,
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

        def on_file_selection(instance, selection):
            if selection:
                popup.dismiss()
                process_sprites_atlas(
                    file_path=selection[0],
                    fila=int(self.fila_input.text),
                    columna_inicial=int(self.columna_input.text) - 1,
                    num_sprites=int(self.num_sprites_input.text),
                    color_fondo=tuple(map(int, self.color_fondo_input.text.split(",")))
                )
            else:
                popup.dismiss()

        file_chooser.bind(on_submit=on_file_selection)
        popup.open()

    def stop_app(self, instance):
        self.stop()


if __name__ == "__main__":
    MainApp().run()

