import fitz  # Это библиотека PyMuPDF
import os 

# Замените 'input.pdf' и 'outputname' на соответствующие значения
input_pdf = 'Авербах_Ю,_Бейлин_М_Азбука_шахмат_1967_1.pdf'
output_base = 'outputname'

# Создаем папку для сохранения изображений
output_folder = 'output_pymupdf_images'
os.makedirs(output_folder, exist_ok=True)

# Открываем PDF-файл
pdf_document = fitz.open(input_pdf)

# Устанавливаем параметры для повышения качества
zoom = 2.0  # Увеличение (можете настроить по вашему усмотрению)
mat = fitz.Matrix(zoom, zoom)

# Итерируемся по страницам и сохраняем их в PNG
for page_number in range(len(pdf_document)):
    page = pdf_document[page_number]
    image = page.get_pixmap(matrix=mat)  # Применяем матрицу для увеличения
    image_path = os.path.join(output_folder, f'{output_base}_{page_number + 1}.png')
    image.save(image_path)

# Закрываем PDF-файл
pdf_document.close()
