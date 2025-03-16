from PIL import Image

# Definir la paleta de colores del MSX
MSX_PALETTE = [
    (0, 0, 0), (0, 0, 255), (255, 0, 0), (255, 0, 255),
    (0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 255, 255),
    (128, 128, 128), (128, 128, 255), (255, 128, 128), (255, 128, 255),
    (128, 255, 128), (128, 255, 255), (255, 255, 128), (192, 192, 192)
]

# Función para encontrar el color más cercano en la paleta MSX
def closest_color(pixel, palette):
    r, g, b, _ = pixel  # Ignorar el canal alfa
    closest_index = 0
    closest_distance = float('inf')
    for i, color in enumerate(palette):
        pr, pg, pb = color
        distance = (r - pr)**2 + (g - pg)**2 + (b - pb)**2  # Distancia euclidiana
        if distance < closest_distance:
            closest_distance = distance
            closest_index = i
    return closest_index

# Función para procesar sprites y generar la salida con 8 valores por línea
def process_sprites_atlas(file_path, fila, columna_inicial, color_fondo, num_sprites):
    image = Image.open(file_path).convert("RGBA")
    width, height = image.size

    # Coordenadas iniciales de la fila
    start_y = fila * 16
    sprites_code = []

    for sprite_index in range(num_sprites):  # Iterar sobre el número de sprites
        start_x = (columna_inicial + sprite_index) * 16  # Calcular columna del sprite actual
        sprite_data = []

        for y in range(16):  # Recorrer filas dentro del sprite
            byte = 0
            for x in range(8):  # Procesar los primeros 8 píxeles por fila
                pixel = image.getpixel((start_x + x, start_y + y))
                color_index = closest_color(pixel, MSX_PALETTE)

                # Ignorar el color de fondo
                if color_index == closest_color(color_fondo, MSX_PALETTE):
                    bit = 0
                else:
                    bit = 1

                # Desplazar bits
                byte = (byte << 1) | bit

            sprite_data.append(byte)

        # Generar una línea de salida para este sprite
        sprites_code.append(f"; Sprite {sprite_index + 1}")
        for i in range(0, len(sprite_data), 8):  # Agrupar en líneas de 8 valores
            line = sprite_data[i:i + 8]
            sprites_code.append(f"    DB {','.join(map(str, line))}")

    # Guardar en un archivo .asm
    with open("sprites_atlas_decimal.asm", "w") as asm_file:
        asm_file.write("\n".join(sprites_code))

    print(f"Código ASM generado para {num_sprites} sprites en formato decimal en 'sprites_atlas_decimal.asm'.")

# Ejemplo de uso
process_sprites_atlas(
    file_path="atlas.tga",  # Ruta de la imagen
    fila=2,                 # Fila donde están los sprites
    columna_inicial=4,      # Columna inicial de los sprites
    color_fondo=(255, 255, 255, 255),  # Color de fondo (RGBA)
    num_sprites=10          # Número total de sprites a procesar
)

