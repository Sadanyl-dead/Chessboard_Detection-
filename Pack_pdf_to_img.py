import os
import fitz


def convert_pdf_to_images(pdf_path, output_folder):
    dpi = 300
    zoom = 3.0
    magnify = fitz.Matrix(zoom, zoom)
    doc = fitz.open(pdf_path)

    for page in doc:
        try:
            pix = page.get_pixmap(matrix=magnify)
            output_file = os.path.join(
                output_folder, f"page-{page.number}.png")
            pix.save(output_file)
        except Exception as e:
            print(f"Error saving {output_file}: {e}")


input_folder = input(
    "Введите путь к папке с PDF-книгами: ")

if not os.path.exists(input_folder):
    print("Указанная папка не существует.")
else:
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, pdf_file)
            book_name = os.path.splitext(pdf_file)[0]
            output_folder = os.path.join(os.path.dirname(pdf_path), book_name)

            os.makedirs(output_folder, exist_ok=True)
            convert_pdf_to_images(pdf_path, output_folder)

print("Конвертация завершена.")
