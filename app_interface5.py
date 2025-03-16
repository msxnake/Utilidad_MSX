# Programa utilidad MSX versión 0008

from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu  # Importación del nuevo MDDropdownMenu en KivyMD 2.0.0
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp  # Para ajustar el tamaño del menú
import os
from process_tga import process_sprites_atlas

# Paleta real del MSX1 con nombres y valores RGB
MSX_PALETTE = [
    {"name": "negro", "rgb": (0, 0, 0)},
    {"name": "azul", "rgb": (0, 0, 170)},
    {"name": "rojo", "rgb": (170, 0, 0)},
    {"name": "magenta", "rgb": (170, 0, 170)},
    {"name": "verde", "rgb": (0, 170, 0)},
    {"name": "cian", "rgb": (0, 170, 170)},
    {"name": "amarillo", "rgb": (170, 85, 0)},
    {"name": "blanco", "rgb": (170, 170, 170)},
    {"name": "gris", "rgb": (85, 85, 85)},
    {"name": "azul claro", "rgb": (85, 85, 255)},
    {"name": "rojo claro", "rgb": (255, 85, 85)},
    {"name": "magenta claro", "rgb": (255, 85, 255)},
    {"name": "verde claro", "rgb": (85, 255, 85)},
    {"name": "cian claro", "rgb": (85, 255, 255)},
    {"name": "amarillo claro", "rgb": (255, 255, 85)},
    {"name": "blanco brillante", "rgb": (255, 255, 255)},
]

class MainApp(MDApp):
    def build(self):
        # Configuración de la ventana principal
        self.title = "Utilidad MSX"
        self.fila = "1"
        self.columna = "1"
        self.num_sprites = "1"
        self.color_fondo = (255, 255, 255)  # Blanco brillante como valor predeterminado

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

        # Menú desplegable para el color de fondo
        color_button = MDButton(
            text="Seleccionar Color de Fondo",
            pos_hint={"center_x": 0.5},
            md_bg_color=self.theme_cls.primary_color,
            text_color=(1, 1, 1, 1),
            on_release=self.open_color_menu
        )
        layout.add_widget(color_button)

        # Botón "Load TGA"
        load_button = MDButton(
            text="Load TGA",
            pos_hint={"center_x": 0.5},
            md_bg_color=self.theme_cls.primary_color,
            text_color=(1, 1, 1, 1),
            on_release=self.open_file_chooser
        )
        layout.add_widget(load_button)

        # Botón "Salir"
        exit_button = MDButton(
            text="Salir",
            pos_hint={"center_x": 0.5},
            md_bg_color=self.theme_cls.error_color,
            text_color=(1, 1, 1, 1),
            on_release=self.stop_app
        )
        layout.add_widget(exit_button)

        # Crear el menú desplegable
        self.color_menu = MDDropdownMenu(
            items=[
                {
                    "text": color["name"],
                    "on_release": lambda x=color["rgb"]: self.set_color_fondo(x),
                }
                for color in MSX_PALETTE
            ],
            width_mult=4
        )

        return layout

    # Abrir el menú para seleccionar el color de fondo
    def open_color_menu(self, instance):
        self.color_menu.caller = instance  # Vincular el menú al botón llamador
        self.color_menu.open()

    # Establecer el color de fondo seleccionado
    def set_color_fondo(self, color_rgb):
        self.color_fondo = color_rgb
        print(f"Color de fondo seleccionado: {self.color_fondo}")
        self.color_menu.dismiss()

    # Abrir el navegador de archivos para seleccionar un archivo TGA
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
                # Llamar a la función de procesamiento con los parámetros seleccionados
                process_sprites_atlas(
                    file_path=selection[0],
                    fila=int(self.fila_input.text),
                    columna_inicial=int(self.columna_input.text) - 1,
                    num_sprites=int(self.num_sprites_input.text),
                    color_fondo=self.color_fondo
                )
            else:
                popup.dismiss()

        file_chooser.bind(on_submit=on_file_selection)
        popup.open()

    # Salir de la aplicación
    def stop_app(self, instance):
        self.stop()


if __name__ == "__main__":
    MainApp().run()

