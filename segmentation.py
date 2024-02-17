import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
from skimage.feature import canny
from skimage.filters import sobel
from skimage.measure import label, regionprops
from skimage.color import label2rgb


script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'res1.png'
file_path = os.path.join(script_dir, file_name)
if not os.path.exists(os.path.join(script_dir,'cut_objects')):
    os.mkdir(os.path.join(script_dir,'cut_objects'))
# Загрузка изображения страницы с шахматной диаграммой
image = io.imread(file_path)

# Преобразование изображения в оттенки серого
gray_image = color.rgb2gray(image)

# Применение оператора Canny для обнаружения границ
edges = canny(gray_image)

# Применение оператора Sobel для улучшения контуров
elevation_map = sobel(gray_image)

# Применение пороговой фильтрации для выделения контуров
binary_elevation_map = elevation_map > 0.05

# Метки соединенных областей
label_image = label(binary_elevation_map)

# Использование regionprops для анализа областей
fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(image)

for idx, region in enumerate(regionprops(label_image)):
    # Отсеиваем маленькие области
    if region.area < 50000:  # Увеличьте этот порог по площади по вашему усмотрению
        continue
    
    min_row, min_col, max_row, max_col = region.bbox
    # Вырезаем объект из оригинального изображения
    object_cutout = image[min_row:max_row, min_col:max_col]

    # Сохраняем объект в отдельный файл
    object_filename = os.path.join(script_dir,f'cut_objects/object_{idx + 1}.png')
    io.imsave(object_filename, object_cutout,format='png', cmap='gray', vmin=100, vmax=255)

    # Отрисовываем прямоугольник вокруг объекта на оригинальном изображении
    rect = plt.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row,
                        fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

# Сохраняем изображение с выделенными объектами
plt.savefig(os.path.join(script_dir, 'output_with_objects.png'), format='png', dpi=300, bbox_inches='tight')
plt.show()
