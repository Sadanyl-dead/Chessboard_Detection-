import subprocess
import os
import keyboard

# Замените 'input.pdf' и 'outputname' на соответствующие значения
input_pdf = input('Enter name of file (.pdf)')
output_base = 'outputname'

# Создаем папку для сохранения изображений
output_folder = 'output_pdftomp_images_'
os.makedirs(output_folder, exist_ok=True)

# Полный путь к выходной папке
output_path = os.path.join(output_folder, output_base)

# Функция для остановки скрипта по нажатию клавиши "Q"
def stop_script(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'q':
        print("Прекращение скрипта...")
        keyboard.unhook_all()
        exit()

# Устанавливаем хук на клавишу "Q" для остановки скрипта
keyboard.on_press(stop_script)

# Вызываем pdftoppm с использованием subprocess
cmd = f'pdftoppm "{input_pdf}" "{output_path}" -png -rx 300 -ry 300'
subprocess.call(cmd, shell=True)
