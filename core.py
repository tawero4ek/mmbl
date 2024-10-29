import threading
import time
import cv2
import mss
import numpy as np
import pygetwindow as gw
import win32api
import win32con

import global_variables


class Logger:
    def __init__(self, prefix=None):
        self.prefix = prefix

    def log(self, data: str):
        if self.prefix:
            print(f"{self.prefix} {data}")
        else:
            print(data)


logger = Logger("[Script]")
game_running = True


def stop_game():
    global game_running
    game_running = False


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def click_random_areas(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        logger.log(f"Не найдено окно: {window_title}")
        return

    window = windows[0]
    window.activate()

    with mss.mss() as sct:
        running = False
        play_again_button_coords = (190, 600)
        game_timer = None
        top_margin = 70  # Top margin to avoid clicking
        bottom_margin = 50  # Bottom margin to avoid clicking

        def toggle_script():
            nonlocal running, game_timer
            running = not running
            logger.log(f'Script running: {running}')
            if not running and game_timer is not None:
                game_timer.cancel()
                game_timer = None

        def click_play_again_button(x, y):
            MyX = window.left + x
            MyY = window.top + y
            click_at(MyX, MyY)

        def game_over():
            nonlocal running, game_timer
            running = False
            game_timer = None
            logger.log('Окончание игры, нажмите кнопку воспроизвести еще раз')
            click_play_again_button(*play_again_button_coords)
            threading.Thread(target=press_and_restart).start()

        def press_and_restart():
            time.sleep(1)
            toggle_script()

        def reset_game_timer():
            nonlocal game_timer
            if game_timer is not None:
                game_timer.cancel()
            game_timer = threading.Timer(50.0, game_over)
            logger.log('Сброс игрового таймера')
            game_timer.start()

        logger.log("Начало работы скрипта")
        while True:
            if global_variables.is_running:
                if game_timer is None or not game_timer.is_alive():
                    reset_game_timer()

                monitor = {
                    "top": window.top + top_margin,
                    "left": window.left,
                    "width": window.width,
                    "height": window.height - top_margin - bottom_margin
                }

                # Клик в случайные координаты в пределах окна, с учётом отступов сверху и снизу
                x = np.random.randint(monitor["left"], monitor["left"] + monitor["width"])
                y = np.random.randint(monitor["top"], min(monitor["top"] + monitor["height"], 690))

                click_at(x, y)

                time.sleep(0.001)  # Ожидание между кликами уменьшено до 0.1 секунды
            else:
                logger.log("Скрипт приостановлен")
                time.sleep(1)
