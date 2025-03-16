# Programa utilidad MSX versión 0003

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from collections import Counter
from PIL import Image
import os


# Paleta real del MSX1 con nombres asociados
MSX_PALETTE = [
    ((0, 0, 0), "negro"),
    ((0, 0, 170), "azul"),
    ((170, 0, 0), "rojo"),
    ((170, 0, 170), "magenta"),
    ((0, 170, 0), "verde"),
    ((0, 170, 170), "cian"),
    ((170, 85, 0), "amarillo"),
    ((170, 170, 170), "blanco"),
    ((85, 85, 85), "gris"),
    ((85, 85, 255), "azul claro"),
    ((255, 85, 85), "rojo claro"),
    ((255, 85, 255), "magenta claro"),
    ((85, 255, 85), "verde claro"),
    ((85, 255, 255), "cian claro"),
    ((255, 255, 85), "amarillo claro"),
    ((255, 255, 255), "blanco brillante")
]

# Función para encontrar el color más cercano y su nombre en la paleta MSX
def closest_color(pixel, palette):
    r, g, b, _ = pixel  # Ignorar el canal alfa
    closest_color = None
    closest_name = None
    closest_distance = float('inf')
    for color, name in palette:
        pr, pg, pb = color
        distance = (r - pr)**2 + (g - pg)**2 + (b - pb)**2  # Distancia euclidiana
        if distance < closest_distance:
            closest_distance = distance
            closest_color = color
            closest_name = name
    return closest_color, closest_name

# Función para obtener los dos colores más frecuentes (excluyendo el color de fondo)
def get_top_two_colors(sprite_pixels, fondo_index):
    filtered_pixels = [color for color in sprite_pixels if color != fondo_index]
    color_counts = Counter(filtered_pixels)
    top_colors = color_counts.most_common(2)
    return [color[0] for color in top_colors]  # Devuelve los dos colores más comunes

# Función para procesar un archivo TGA
def process_sprites_atlas(file_path, fila, columna_inicial, num_sprites, color_fondo):
    image = Image.open(file_path).convert("RGBA")
    width, height = image.size

    # Coordenadas iniciales de la fila
    start_y = fila * 16
    sprites_code = []

    for sprite_index in range(num_sprites):  # Iterar sobre el número de sprites
        start_x = (columna_inicial + sprite_index) * 16  # Calcular columna del sprite actual

        # Extraer los píxeles del sprite
        sprite_pixels = []
        for y in range(16):  # Filas dentro del sprite
            for x in range(16):  # Columnas dentro del sprite
                pixel = image.getpixel((start_x + x, start_y + y))
                color_index, _ = closest_color(pixel, MSX_PALETTE)
                sprite_pixels.append(color_index)

        # Obtener el índice del color de fondo
        fondo_index, _ = closest_color(color_fondo, MSX_PALETTE)

        # Obtener los dos colores más comunes (excluyendo el fondo)
        color1, color2 = get_top_two_colors(sprite_pixels, fondo_index)
        _, color1_name = closest_color(color1, MSX_PALETTE)
        _, color2_name = closest_color(color2, MSX_PALETTE)

        # Generar datos para cada color
        for color, name in [(color1, color1_name), (color2, color2_name)]:
            sprites_code.append(f"; Sprite {sprite_index + 1}, color = {name}")
            sprite_data = []

            for y in range(16):  # Filas dentro del sprite
                byte = 0
                for x in range(8):  # Procesar los primeros 8 píxeles por fila
                    pixel_index = (y * 16) + x
                    if sprite_pixels[pixel_index] == color:
                        bit = 1
                    else:
                        bit = 0

                    # Desplazar bits
                    byte = (byte << 1) | bit

                sprite_data.append(byte)

            # Agrupar en líneas de 8 valores y añadir al ASM
            for i in range(0, len(sprite_data), 8):
                line = sprite_data[i:i + 8]
                sprites_code.append(f"    DB {','.join(map(str, line))}")

    # Guardar en un archivo .asm
    with open("sprites_atlas_named_colors.asm", "w") as asm_file:
        asm_file.write("\n".join(sprites_code))

    print(f"Código ASM generado para {num_sprites} sprites con nombres de colores en 'sprites_atlas_named_colors.asm'.")

# Función que conecta el archivo elegido con el procesamiento
def process_tga_file(file_path):
    print(f"Procesando archivo TGA: {file_path}")
    # Llamar a process_sprites_atlas con parámetros ejemplo
    process_sprites_atlas(
        file_path=file_path,
        fila=2,  # Modifica según sea necesario
        columna_inicial=4,  # Modifica según sea necesario
        num_sprites=10,  # Modifica según sea necesario
        color_fondo=(255, 255, 255, 255)  # Blanco brillante como fondo
    )

# Clase principal de la aplicación
class MainApp(MDApp):
    def build(self):
        # Configuración de la ventana principal
        self.title = "Utilidad MSX"
        Window.size = (600, 400)

        # Layout principal
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Etiqueta del título
        title_label = MDLabel(
            text="Utilidad MSX",
            halign="center",
            theme_text_color="Primary",
            font_style="H5"
        )
        layout.add_widget(title_label)

        # Botón "Load TGA"
        load_button = MDRaisedButton(
            text="Load TGA",
            pos_hint={"center_x": 0.5},
            on_release=self.open_file_chooser
        )
        layout.add_widget(load_button)

        # Botón "Salir"
        exit_button = MDRaisedButton(
            text="Salir",
            pos_hint={"center_x": 0.5},
            on_release=self.stop_app
        )
        layout.add_widget(exit_button)

        return layout

    # Abrir el navegador de archivos para seleccionar un archivo TGA
    def open_file_chooser(self, instance):
        file_chooser = FileChooserListView(filters=["*.tga"], path=os.getcwd())
        popup = Popup(
            title="Seleccionar archivo TGA",
            content=file_chooser,
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

        # Acción al seleccionar un archivo
        def on_file_selection(instance, selection):
            if selection:  # Verificar que se seleccionó un archivo
                popup.dismiss()
                process_tga_file(selection[0])  # Llamar a la función de procesamiento
            else:
                popup.dismiss()

        # Vincular evento de selección
        file_chooser.bind(on_submit=on_file_selection)
        popup.open()

    # Salir de la aplicación
    def stop_app(self, instance):
        self.stop()


# Ejecutar la aplicación
if __name__ == "__main__":
    MainApp().run()

