import sys
import threading

from core import click_color_areas
from gui import create_and_run_gui


if __name__ == "__main__":
    target_colors_hex = ["#c5d900", "#7eff22"]

    try:
        # Поток логики
        worker_thread1 = threading.Thread(target=click_color_areas, args=("TelegramDesktop", target_colors_hex))
        worker_thread1.daemon = True
        worker_thread1.start()

        # Поток графики
        worker_thread2 = threading.Thread(target=create_and_run_gui)
        worker_thread2.daemon = True
        worker_thread2.start()

        # Если графическое окно было закрыто, завершаем всю программу
        if not worker_thread2.is_alive():
            print("Графическое окно было закрыто, завершаем программу...")
            sys.exit()
        else:
            worker_thread2.join()
            print("Завершение программы...")
            sys.exit()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)
