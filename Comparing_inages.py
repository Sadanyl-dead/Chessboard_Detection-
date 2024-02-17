from PIL import Image
import os
import shutil

# Папка с исходными изображениями
source_folder = "D:\\UNIC\\diplom\\cut_objects"

# Создаем новую папку для сохранения отфильтрованных изображений
output_folder = "cut_and_filtered"
os.makedirs(output_folder, exist_ok=True)

# Эталонные размеры
etalon_min_width = 300
etalon_min_height = 300
etalon_max_width = 370
etalon_max_height = 370

# Функция для фильтрации изображений
def filter_images(source_folder, output_folder, min_width, min_height, max_width, max_height):
    for filename in os.listdir(source_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            image_path = os.path.join(source_folder, filename)
            image = Image.open(image_path)
            image_width, image_height = image.size

            if (min_width <= image_width <= max_width) and (min_height <= image_height <= max_height):
                shutil.copy(image_path, os.path.join(output_folder, filename))

# Вызываем функцию для фильтрации изображений
filter_images(source_folder, output_folder, etalon_min_width, etalon_min_height, etalon_max_width, etalon_max_height)

print("Изображения, которые находятся в диапазоне размеров от 300x300 до 370x370, сохранены в папку 'cut_and_filtered'.")
