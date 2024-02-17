import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, transform
from skimage.feature import canny
from skimage.filters import sobel
from skimage.measure import label, regionprops
from skimage.metrics import mean_squared_error

script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, 'books')
output_folder = os.path.join(script_dir, 'cut_objects')
output_objects_folder = os.path.join(script_dir, 'output_objects')

reference_image_path = os.path.join(script_dir, 'reference_image.png')
mse_threshold = 4000.0

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

if not os.path.exists(output_objects_folder):
    os.mkdir(output_objects_folder)


def mse(image1, image2):
    return mean_squared_error(image1, image2)


reference_image = io.imread(reference_image_path)
reference_gray = color.rgb2gray(reference_image)
reference_shape = reference_gray.shape


def process_image(image, output_dir, min_area=20000):
    gray_image = color.rgb2gray(image)
    edges = canny(gray_image)
    elevation_map = sobel(gray_image)
    binary_elevation_map = elevation_map > 0.05
    label_image = label(binary_elevation_map)

    for idx, region in enumerate(regionprops(label_image)):
        if region.area < min_area:
            continue

        min_row, min_col, max_row, max_col = region.bbox
        object_cutout = image[min_row:max_row, min_col:max_col]
        object_gray = color.rgb2gray(object_cutout)

        if object_gray.shape != reference_shape:
            object_gray = transform.resize(
                object_gray, reference_shape, anti_aliasing=True)

        object_mse = mse(object_gray, reference_gray)

        if object_mse <= mse_threshold:
            object_filename = os.path.join(
                output_dir, f'object_page_{idx + 1}.png')
            io.imsave(object_filename, object_cutout, format='png',
                      cmap='gray', vmin=100, vmax=255)

            rect = plt.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row,
                                 fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

    return ax


for book_folder in os.listdir(input_folder):
    book_folder_path = os.path.join(input_folder, book_folder)
    if os.path.isdir(book_folder_path):
        for filename in os.listdir(book_folder_path):
            if filename.endswith(".png"):
                file_path = os.path.join(book_folder_path, filename)
                image = io.imread(file_path)

                fig, ax = plt.subplots(figsize=(8, 6))
                ax.imshow(image)

                process_image(image, output_folder)

                output_filename = os.path.join(
                    output_objects_folder, f'output_with_objects_{filename}')
                plt.savefig(output_filename, format='png',
                            dpi=300, bbox_inches='tight')
                plt.close()
