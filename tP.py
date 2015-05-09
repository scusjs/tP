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

presentation_content = [{"content" : [{"content":"test", "attribute" : ""}, {"content" : "你好世界" , "attribute" : ""}], "attribute" : "body"}, {"content" : [{"content" : "int a;", "attribute" : ""}, {"content" : "int b;", "attribute" : ""}], "attribute" : "code"}, {"content" : [{"content" : "scu.jpg", "attribute" : ""}], "attribute" : "image"}, {"content" : [{"content" : "hello world", "attribute" : ""}], "attribute" : "session"}]

class TerminalPresentation:
    def __init__(self):
        self.currentpath = os.getcwd()
        self.screen = curses.initscr()
        curses.cbreak()
        self.height, self.width = self.screen.getmaxyx()
        self.show_str(" ", 0, True)
        for i in presentation_content:
            self.show_page(i)
        self.screen.getch()
        curses.endwin()

    def show_page(self, page_info):
        page_attribute = page_info["attribute"]
        page_content = page_info["content"]
        self.__reset_background()
        self.__clr()
        if page_attribute == "session":
            start_y = self.__get_start_y(len(page_content) + 2)
            self.show_str("======❧❦☙======", start_y, False)
            self.show_str("======❧❦☙======", start_y + len(page_content) + 1, False)
            for i in range(0, len(page_content)):
                content_txt = page_content[i]["content"]
                self.show_str(content_txt, start_y + i + 1, True)
        if page_attribute == "image":
            image_path = page_info["content"][0]["content"]
            self.__set_background(image_path)


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

    def __get_start_y(self, content_len):
        return int((self.height - content_len) / 2)


if __name__ == "__main__":
    tp = TerminalPresentation()
