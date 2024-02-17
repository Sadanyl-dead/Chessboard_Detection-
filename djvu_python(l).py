import os
import subprocess
from langdetect import detect
from googletrans import Translator

# Функция для замены пробелов на нижние подчеркивания


def process_book_name(book_name):
    return book_name.replace(" ", "_")

# Функция для перевода названия на английский без пробелов


def translate_to_english(book_name):
    translator = Translator()
    translated = translator.translate(book_name, dest="en")
    # Удаляем пробелы из переведенного названия
    translated_text = translated.text.replace(" ", "")
    return translated_text

# Функция для конвертирования книги в PDF


def convert_to_pdf(book_name):
    # Включаем путь к книге в имя
    full_book_name = os.path.join(folder_path, f"{book_name}.djvu")
    processed_name = translate_to_english(process_book_name(full_book_name))

    # Папку djvu-pdf создаем только один раз перед началом операций
    output_folder = "djvu-pdf"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Формирование команды ddjvu
    ddjvu_command = [
        "C:\\Program Files (x86)\\DjVuLibre\\ddjvu.exe",
        "-format=pdf",
        full_book_name,
        os.path.join(output_folder, f"{processed_name}.pdf")
    ]

    try:
        subprocess.run(ddjvu_command)
        print(
            f"Конвертация завершена: {full_book_name} -> {processed_name}.pdf")
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")


# Опция для выбора действия
print("Выберите действие:")
print("1. Перевести и конвертировать все книги в папке")
print("2. Конвертировать одну книгу")

choice = input("Введите номер действия (1 или 2): ")

if choice == "1":
    folder_path = input(
        "Введите путь к папке с книгами (или нажмите Enter для стандартного пути D:\\UNIC\\diplom\\djvu_books): ")
    if folder_path == "":
        # Укажите здесь стандартный путь
        folder_path = "D:\\UNIC\\diplom\\djvu_books"
    book_list = [f for f in os.listdir(folder_path) if f.endswith(".djvu")]

    for book_name in book_list:
        book_name_without_extension = os.path.splitext(book_name)[0]
        new_name = translate_to_english(
            process_book_name(book_name_without_extension))
        os.rename(os.path.join(folder_path, book_name), os.path.join(
            folder_path, f"{new_name}.djvu"))
        convert_to_pdf(new_name)
elif choice == "2":
    folder_path = input(
        "Введите путь к папке с книгами (или нажмите Enter для стандартного пути D:\\UNIC\\diplom\\djvu_books): ")
    if folder_path == "":
        # Укажите здесь стандартный путь
        folder_path = "D:\\UNIC\\diplom\\djvu_books"
    book_name = input(
        "Введите название книги (без .djvu): ")
    book_name_without_extension = os.path.splitext(book_name)[0]
    new_name = translate_to_english(
        process_book_name(book_name_without_extension))
    os.rename(os.path.join(folder_path, book_name), os.path.join(
        folder_path, f"{new_name}.djvu"))
    convert_to_pdf(new_name)
else:
    print("Некорректный выбор. Пожалуйста, введите 1 или 2.")
