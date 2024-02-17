import cv2
import numpy as np
from matplotlib import pyplot as plt

# Try to load the image and handle any potential errors
try:
    image_path = 'C:\\Users\\dansp\\Desktop\\diplom\\sd.png'
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("Image not loaded. Check the file path.")
except Exception as e:
    print("Error:", e)
    image = None

# Proceed only if the image was loaded successfully
if image is not None:
    image = np.flip(image, axis=-1)
    bw_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    images = [image, bw_img]

    titles = ['Обычное', 'ЧБ']

    for i in range(len(images)):
        plt.subplot(1, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    plt.show()
    cv2.imwrite('C:\\Users\\dansp\\Desktop\\diplom\\bw_img.jpeg', bw_img)
