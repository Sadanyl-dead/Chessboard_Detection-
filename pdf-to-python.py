import os
import fitz

script_dir = r'C:\Users\Sadanyl\Desktop\укапыв'
file_name = 'Y&Y FZE Summary sheet.pdf'
file_path = os.path.join(script_dir, file_name)
dpi = 300  # выберите желаемое разрешение здесь
zoom = 3.0  # увеличьте этот параметр для улучшения качества
# увеличивает в x и y направлениях
magnify = fitz.Matrix(zoom, zoom)
doc = fitz.open(file_path)  # открываем документy

# Создаем папку для сохранения изображений, используя имя книги
output_folder = os.path.join(script_dir, file_name.replace('.pdf', ''))
os.makedirs(output_folder, exist_ok=True)

for page in doc:
    try:
        # рендерим страницу в изображение
        pix = page.get_pixmap(matrix=magnify)
        output_file = os.path.join(output_folder, f"page-{page.number}.png")
        pix.save(output_file)
    except Exception as e:
        print(f"Error saving {output_file}: {e}")
