import customtkinter as ctk
import keyboard
import global_variables


def update_button_state(button):
    button_text = "Остановить майнер\n\nНажми Пробел" if global_variables.is_running else "Запустить майнер\n\nНажми Пробел"
    if global_variables.is_running:
        button_color = "pink"
    else:
        button_color = "green"
    button.configure(text=button_text, fg_color=button_color, text_color="black")


def toggle_is_running(button):
    global_variables.is_running = not global_variables.is_running
    # button_text = "Остановить майнер\n\nНажми Пробел" if global_variables.is_running else "Запустить майнер\n\nНажми Пробел"
    update_button_state(button)
    return global_variables.is_running


def handle_space_press(event):
    toggle_is_running(button)


def create_and_run_gui():
    global root, button

    ctk.set_appearance_mode("dark")  # Включение темной темы
    ctk.set_default_color_theme("blue")  # Установка синей темы по умолчанию

    root = ctk.CTk()
    root.title("БлумМайнер999")
    root.geometry("265x300")

    # Запретить изменение размера окна
    root.resizable(False, False)

    # button_text = "Остановить майнер\n\nНажми Пробел" if global_variables.is_running else "Запустить майнер\n\nНажми Пробел"
    # button = ctk.CTkButton(root, text=button_text, command=lambda: toggle_is_running(button), height=5)

    button = ctk.CTkButton(root, command=lambda: toggle_is_running(button), height=5)
    update_button_state(button)
    button.pack(fill='x', padx=20, pady=70)

    # Создание кнопки для открытия диалогового окна
    dialog_button = ctk.CTkButton(root, text="Info", command=show_dialog)
    dialog_button.pack(fill='x', padx=20, pady=20)

    # Связывание нажатия на пробел с функцией handle_space_press
    # root.bind("<space>", handle_space_press)
    # Установка глобального обработчика нажатия пробела
    keyboard.add_hotkey('space', lambda: handle_space_press(None))

    root.resizable(False, False)
    # Сделать окно поверх всех других окон
    root.wm_attributes("-topmost", 1)

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 265
    window_height = 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.mainloop()


def show_dialog():
    dialog = ctk.CTkToplevel(root)
    dialog.title("Информация")
    dialog.geometry("300x200")
    dialog.resizable(False, False)

    # Создание элементов диалогового окна
    label = ctk.CTkLabel(dialog, text=
    "1) Запускаем блум,\nа только потом запускаем exe-шник!\n"
    "2) Закрываем основное окно телеги (опционально)\n"
    "3) Нажимаем 'Запустить майнер'\n"
    "4) Для остановки нажимаем пробел'\n\n"
    "Автоматический кликер V1.08.\n"
    "Совместная разработка Чепусова и Яцышина\n"
    "2024 год",
                         wraplength=280, justify="left")
    label.pack(pady=10)

    close_button = ctk.CTkButton(dialog, text="Закрыть", command=dialog.destroy)
    close_button.pack(pady=10)
    dialog.wm_attributes("-topmost", 1)
    dialog.mainloop()
