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


def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    rgb_normalized = np.array([[rgb]], dtype=np.uint8)
    hsv = cv2.cvtColor(rgb_normalized, cv2.COLOR_RGB2HSV)
    return hsv[0][0]


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def click_color_areas(window_title, target_colors_hex):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        logger.log(f"No window found with title: {window_title}")
        return

    window = windows[0]
    window.activate()

    target_hsvs = [hex_to_hsv(color) for color in target_colors_hex]

    with mss.mss() as sct:
        running = False
        play_again_button_coords = (190, 600)  # изменяется ли окно телеги?
        game_timer = None
        backtick_timer = None

        def toggle_script():
            nonlocal running, game_timer, backtick_timer
            running = not running
            logger.log(f'Script running: {running}')
            if not running:
                if game_timer is not None:
                    game_timer.cancel()
                    game_timer = None
                if backtick_timer is not None:
                    backtick_timer.cancel()
                    backtick_timer = None

        def click_play_again_button(x, y):
            MyX = window.left + x
            MyY = window.top + y
            click_at(MyX, MyY)

        def game_over():
            nonlocal running, game_timer
            running = False
            game_timer = None
            logger.log('Game over detected, clicking play again button')
            click_play_again_button(*play_again_button_coords)
            threading.Thread(target=press_and_restart).start()

        def press_and_restart():
            # press_backtick()
            time.sleep(1)
            toggle_script()

        def reset_game_timer():
            nonlocal game_timer
            if game_timer is not None:
                game_timer.cancel()
            game_timer = threading.Timer(40.0, game_over)
            logger.log('Game timer reset')
            game_timer.start()

        while True:
            if global_variables.is_running:
                if game_timer is None or not game_timer.is_alive():
                    reset_game_timer()

                monitor = {
                    "top": window.top,
                    "left": window.left,
                    "width": window.width,
                    "height": window.height
                }
                img = np.array(sct.grab(monitor))

                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

                for target_hsv in target_hsvs:
                    lower_bound = np.array([max(0, target_hsv[0] - 5), 50, 50])
                    upper_bound = np.array([min(179, target_hsv[0] + 5), 255, 255])

                    mask = cv2.inRange(hsv, lower_bound, upper_bound)

                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    for contour in contours:
                        if cv2.contourArea(contour) < 300:
                            continue

                        M = cv2.moments(contour)
                        if M["m00"] == 0:
                            continue
                        cX = int(M["m10"] / M["m00"]) + monitor["left"]
                        cY = int(M["m01"] / M["m00"]) + monitor["top"]

                        click_offset_y = 0
                        click_at(cX, cY + click_offset_y)
                        logger.log(f'Clicked: {cX} {cY + click_offset_y}')
            else:
                time.sleep(1)
