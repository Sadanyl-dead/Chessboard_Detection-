import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
# разобратсья с контурами картинки


script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'object_116.png'
file_path = os.path.join(script_dir, file_name)
image_path = os.path.join(script_dir, file_name)
img = cv2.imread(image_path)

# Определение ядра свертки
morph_kernel = np.ones((2, 2))

# Применение функций к изображению
# Параметр iterations означает, сколько раз будет применена операция
dilate_img = cv2.dilate(img, kernel=morph_kernel, iterations=1)
erode_img = cv2.erode(img, kernel=morph_kernel, iterations=1)
# араметром ksize=(11, 11) зададим размер ядра фильтра размытия 11х11 пикселей:
# параметры sigmaX/Y 0, 0 отвечают за сдвиг ядра при проходе по осям X, Y
blurred_img = cv2.GaussianBlur(img, ksize=(1, 1), sigmaX=0, sigmaY=0)
sharp_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

# параметр ddepth отвечает за «глубину» картинки
# ddepth=-1 означает, что глубина получившейся картинки будет как у исходной
sharpen_img = cv2.filter2D(img, ddepth=-1, kernel=sharp_filter)

if img is not None:
    images = [img, dilate_img, erode_img, blurred_img, sharpen_img]

    titles = ['Обычное', 'Dilate', 'Erode', 'Blured', 'Sharpen']

    for i in range(len(images)):
        plt.subplot(1, 5, i+1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    # Преобразуем изображение в оттенки серого
    gray_erode_img = cv2.cvtColor(erode_img, cv2.COLOR_BGR2GRAY)

    # Находим контуры на изображении
    contours, _ = cv2.findContours(
        gray_erode_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Отрисовываем контуры на изображении
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

    plt.figure()
    plt.imshow(img, 'gray')
    plt.title('Контуры')
    plt.xticks([]), plt.yticks([])

    plt.show()

    # Сохраняем изображение с контурами (разобраться с черным и белым - vmin vmax)
    cv2.imwrite(os.path.join(script_dir, 'sharpen_img1.png'),
                format='png', cmap='gray', vmin=100, vmax=255)
