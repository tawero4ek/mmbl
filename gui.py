import tkinter as tk
import os
import keyboard
import global_variables


def set_background_image(image_name, root):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "images", image_name)
    background_image = tk.PhotoImage(file=image_path)
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    return background_image


def toggle_is_running(button):
    # global is_running
    global_variables.is_running = not global_variables.is_running
    button_text = "Остановить майнер\n\nНажми Пробел" if global_variables.is_running else "Запустить майнер\n\nНажми Пробел"
    button.config(text=button_text)
    return global_variables.is_running


def handle_space_press(event):
    toggle_is_running(button)


def create_and_run_gui():
    global root, button

    root = tk.Tk()
    root.title("БлумМайнер999")
    root.geometry("265x300")

    # Запретить изменение размера окна
    root.resizable(False, False)
    background_image = set_background_image("bg.png", root)


    button_text = "Остановить майнер\n\nНажми Пробел" if global_variables.is_running else "Запустить майнер\n\nНажми Пробел"
    button = tk.Button(root, text=button_text, command=lambda: toggle_is_running(button), height=5)
    button.pack(fill='x', padx=20, pady=70)


    # Создание кнопки для открытия диалогового окна
    dialog_button = tk.Button(root, text="Info", command=show_dialog)
    dialog_button.pack(fill='x', padx=20, pady=20)  # Добавлен отступ сверху и снизу для кнопки диалога



    # Связывание нажатия на пробел с функцией handle_space_press
    #root.bind("<space>", handle_space_press)
    # Установка глобального обработчика нажатия пробела
    keyboard.add_hotkey('space', lambda: handle_space_press(None))

    root.resizable(False, False)
    # Сделать окно поверх всех других окон
    root.wm_attributes("-topmost", 1)
    root.mainloop()



# Функция для создания и отображения диалогового окна
def show_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Информация")
    dialog.geometry("300x150")
    dialog.resizable(False, False)

    # Создание элементов диалогового окна
    label = tk.Label(dialog, text=
                                  "1)Запускаем блум\n"
                                  "2)Закрываем основное окно телеги\n"
                                  "3)Нажимаем 'Запустить майнер'\n"
                                  "4)Для остановки нажимаем пробе'\n"
                                  "Автоматический кликер V1.08.\n\n"
                                  "Совместная разработка Чепусова и Яцышина\n"
                                  "2024 год \n"
                     )
    label.pack(pady=20)

    button = tk.Button(dialog, text="Закрыть", command=dialog.destroy)
    button.pack(pady=10)
    dialog.wm_attributes("-topmost", 1)
    # Ожидание закрытия диалогового окна
    dialog.wait_window()