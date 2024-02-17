# Импорт необходимых библиотек и модулей
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, transform
from skimage.feature import canny
from skimage.filters import sobel
from skimage.measure import label, regionprops
from skimage.metrics import mean_squared_error

# Определение пути к текущей директории скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к папке с изображениями для обработки
input_folder = os.path.join(script_dir, 'books/bologgan_v__slavyanskaya_protection._system_chebanenko_(2006).Djvu')

# Путь к папке для сохранения обработанных изображений
output_folder = os.path.join(script_dir, 'cut_objects')

# Путь к эталонному изображению
reference_image_path = os.path.join(script_dir, 'reference_image.png')

# Порог среднеквадратичной ошибки
mse_threshold = 4000.0

# Проверяем существование папки для сохранения обработанных изображений
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Функция для вычисления среднеквадратичной ошибки между двумя изображениями
def mse(image1, image2):
    return mean_squared_error(image1, image2)

# Загрузка эталонного изображения и преобразование его в оттенки серого
reference_image = io.imread(reference_image_path)
reference_gray = color.rgb2gray(reference_image)
reference_shape = reference_gray.shape

# Функция для обработки каждого изображения
# Функция для обработки каждого изображения
def process_image(image, output_dir, min_area=20000):
    # Преобразование изображения в оттенки серого
    gray_image = color.rgb2gray(image)
    
    # Применение фильтра Canny для детектирования границ
    edges = canny(gray_image)
    
    # Вычисление элевации изображения с помощью оператора Собеля
    elevation_map = sobel(gray_image)
    
    # Преобразование элевации в двоичное изображение
    binary_elevation_map = elevation_map > 0.05
    
    # Сегментация изображения и присвоение меток
    label_image = label(binary_elevation_map)

    # Обработка каждой области на изображении
    for idx, region in enumerate(regionprops(label_image)):
        # Пропускаем области с площадью меньше минимальной
        if region.area < min_area:
            continue
        
        # Выделение области из изображения
        min_row, min_col, max_row, max_col = region.bbox
        object_cutout = image[min_row:max_row, min_col:max_col]
        
        # Преобразование выделенной области в оттенки серого
        object_gray = color.rgb2gray(object_cutout)

        # Проверка размера объекта и его преобразование к размеру эталонного изображения при необходимости
        if object_gray.shape != reference_shape:
            object_gray = transform.resize(object_gray, reference_shape, anti_aliasing=True)

        # Вычисление среднеквадратичной ошибки между объектом и эталонным изображением
        object_mse = mse(object_gray, reference_gray)

        # Проверка среднеквадратичной ошибки и сохранение объекта, если он "похож" на эталонное изображение
        if object_mse <= mse_threshold:
            object_filename = os.path.join(output_dir, f'object_{idx + 1}.png')
            io.imsave(object_filename, object_cutout, format='png', cmap='gray', vmin=100, vmax=255)

            # Отрисовка прямоугольника вокруг объекта на оригинальном изображении
            rect = plt.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

    return ax


# Обработка каждого изображения в целевой папке
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        file_path = os.path.join(input_folder, filename)
        image = io.imread(file_path)

        # Создание графического окна для текущего изображения
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(image)

        # Обработка изображения и сохранение обработанного изображения с выделенными объектами
        process_image(image, output_folder)

        output_filename = os.path.join(output_folder, f'output_with_objects_{filename}')
        plt.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')
        plt.close()
