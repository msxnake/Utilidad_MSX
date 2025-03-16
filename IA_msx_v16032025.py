# Programa utilidad MSX versión 0001

from PIL import Image
from collections import Counter

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

# Función principal
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

# Ejemplo de uso
process_sprites_atlas(
    file_path="atlas.tga",  # Ruta de la imagen
    fila=2,                 # Fila donde están los sprites
    columna_inicial=4,      # Columna inicial de los sprites
    num_sprites=10,         # Número total de sprites a procesar
    color_fondo=(255, 255, 255, 255)  # Color de fondo (RGBA)
)

