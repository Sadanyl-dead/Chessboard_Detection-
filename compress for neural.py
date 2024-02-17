import os
from PIL import Image

# Папка с изображениями, которые нужно сжать
input_folder = "mix"

# Папка, куда будут сохраняться сжатые изображения
output_folder = "neural study samples"

# Коэффициент сжатия (меньше 1.0 для уменьшения размера)
compression_ratio = 0.9

# Качество сжатых изображений (0-100)
compression_quality = 90

# Создаем выходную папку, если её нет
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
i = 0
# Проходим по всем файлам в папке mix
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)

        # Получаем новое имя файла для сжатого изображения
        new_filename = os.path.splitext(filename)[0] + "_compressed.jpg"
        output_path = os.path.join(output_folder, new_filename)

        # Получаем новые размеры изображения с учетом коэффициента сжатия
        new_width = int(image.width * compression_ratio)
        new_height = int(image.height * compression_ratio)

        # Сжимаем изображение и сохраняем
        img = image.resize((new_width, new_height), Image.LANCZOS)
        img.save(output_path, "JPEG", quality=compression_quality)
        i += 1
        print(f"Сжато: {image_path} -> {output_path}")
        print(f"Всего сжато изображений {i}")
