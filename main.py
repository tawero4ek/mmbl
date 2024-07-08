import sys
import threading
from core import click_random_areas
from gui import create_and_run_gui

if __name__ == "__main__":
    try:
        # Поток логики
        worker_thread1 = threading.Thread(target=click_random_areas, args=("TelegramDesktop",))
        worker_thread1.daemon = True
        worker_thread1.start()

        # Поток графики
        worker_thread2 = threading.Thread(target=create_and_run_gui)
        worker_thread2.daemon = True
        worker_thread2.start()

        # Ожидание завершения потока графического интерфейса
        worker_thread2.join()
        print("Графическое окно было закрыто, завершаем программу...")
        sys.exit(0)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)
