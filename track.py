# coding=utf-8
import json
import logging

import time
from pynput.mouse import Controller, Button, Listener as MouseLister

with open('config') as file:
    config = json.loads(file.read())
LOG_DIC = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, 'ERROR': logging.ERROR}

logging.basicConfig(level=LOG_DIC[config['LOG_LEVEL']])


class WriteTrack():
    def __init__(self):
        if config['OVERRIDE'] is True:
            open('track.txt', 'w')
        self.track_list = []

    def mouse_on_move(self, x, y):
        logging.debug('mouse Moved to {0}'.format((x, y)))
        self.track_list.append('{0}:{1},{2}'.format('Position', x, y))

    def mouse_on_click(self, x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        logging.debug('{0} at {1}'.format(action, (x, y)))
        self.track_list.append('{0}:{1},{2}'.format(action, x, y))
        if not pressed:
            track_file = open('track.txt', 'a')
            for t in self.track_list:
                track_file.write(t + '\n')
            track_file.close()
            return False

    def mouse_on_scroll(self, x, y, dx, dy):
        logging.debug('mouse Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))


class ReadTrack():
    def read_track(self):
        with open('track.txt') as fr:
            for track in fr:
                action, coord = track.split(':')
                coord_x, coord_y = coord.split(',')
                mouse = Controller()
                if action == 'Position':
                    mouse.position = (float(coord_x), float(coord_y))
                elif action == 'Pressed':
                    mouse.click(Button.left)
                    mouse.press(Button.left)
                elif action == 'Released':
                    mouse.release(Button.left)
                time.sleep(0.01)


if __name__ == '__main__':
    # 记录鼠标操作
    write = WriteTrack()
    with MouseLister(on_move=write.mouse_on_move, on_click=write.mouse_on_click,
                     on_scroll=write.mouse_on_scroll) as listener:
        listener.join()

    #读取鼠标操作
    # read = ReadTrack()
    # read.read_track()
