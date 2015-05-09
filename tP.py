#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file tP.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2015-05-09

import curses
import os
from time import sleep
import locale

locale.setlocale(locale.LC_ALL, '')
default_line_time = 1

class TerminalPresentation:
    def __init__(self):
        self.currentpath = os.getcwd()
        self.screen = curses.initscr()
        curses.cbreak()
        self.height, self.width = self.screen.getmaxyx()
        self.show_str(" ", 0, True)
        self.show_str("test", 5, True)
        self.show_str("你好世界", 6, True)
        self.show_str("======❧❦☙=====", 7, True)
        self.__clr()
        self.__set_background("scu.jpg")
        sleep(2)
        self.__reset_background()
        self.show_str("这是第二页", 7, True)
        self.screen.getch()
        curses.endwin()

    def show_str(self, printstr, height, sleep):
        start_x = self.__get_start_x(printstr)
        if sleep == True:
            self.__print_with_sleep(printstr, start_x, height)
        else:
            self.__print_without_sleep(printstr, start_x, height)

    def __print_with_sleep(self, printstr, start_x, start_y):
        strlen = len(printstr)
        for i in range(0, strlen):
            if self.__is_cn_char(printstr[i]):
                self.__print_char(start_y, start_x + i * 2, printstr[i])
            else:
                self.__print_char(start_y, start_x + i, printstr[i])
            sleep(float(default_line_time) / strlen)

    def __print_without_sleep(self, printstr, start_x, start_y):
        self.screen.addstr(start_y, start_x, printstr)

    def __clr(self):
        self.screen.clear()
        self.screen.refresh()

    def __print_char(self, y, x, char):
        self.screen.addstr(y, x, char)
        self.screen.refresh()

    def __set_background(self, path):
        set_back_str = "osascript -e \'tell application \"iTerm\" to set background image path of current session of current terminal to \"" + self.currentpath + "/" +path + "\"\'"
        os.system(set_back_str)

    def __reset_background(self):
        set_back_str = "osascript -e \'tell application \"iTerm\" to set background image path of current session of current terminal to \"\"\'"
        os.system(set_back_str)

    def __is_cn_char(self, i):
            return 0x4e00<=ord(i)<0x9fa6

    def __get_start_x(self, printstr):
        strlen = len(printstr)
        start_x = strlen
        for i in range(0, strlen):
            if self.__is_cn_char(printstr[i]):
                start_x += 1
        return int((self.width - start_x) / 2)


if __name__ == "__main__":
    tp = TerminalPresentation()
