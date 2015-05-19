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
import sys
from time import sleep
import locale
from content import Content

locale.setlocale(locale.LC_ALL, '')
default_line_time = 0.5

class TerminalPresentation:
    def __init__(self, file_path):
        self.__init_win()
        content = Content(file_path)
        self.image_path = os.path.dirname(file_path)
        self.presentation_content = content.get_content_list()
        self.currentpath = os.getcwd()
        try:
            self.show_str("tP by jinsheng, press 'j' to continue", 0, False)
            self.start()
        except KeyboardInterrupt:
            pass
        self.__reset_background()
        curses.endwin()
    
    def __init_win(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        self.height, self.width = self.screen.getmaxyx()

    def start(self):
        key = 0
        page_size = len(self.presentation_content)
        current_page = -1
        while True:
            if key == ord('q'):
                break
            elif key in (ord('j'), curses.KEY_DOWN, curses.KEY_RIGHT):
                self.__page_duang_after(self.presentation_content[current_page]["attribute"])
                if current_page < page_size - 1:
                    current_page += 1
                self.show_page(self.presentation_content[current_page])
            elif key in (ord('k'), curses.KEY_UP, curses.KEY_LEFT):
                if current_page > 0:
                    current_page -= 1
                elif current_page == -1:
                    current_page = 0
                self.show_page(self.presentation_content[current_page])


            key = self.screen.getch()

    def show_page(self, page_info):
        page_attribute = page_info["attribute"]
        page_content = page_info["content"]
        self.__reset_background()
        self.__page_duang_before(page_attribute)
        if "session" in page_attribute:
            start_y = self.__get_start_y(len(page_content) + 4)
            self.show_str("======❧❦☙======", start_y, False)
            self.show_str("======❧❦☙======", start_y + len(page_content) + 3, False)
            for i in range(0, len(page_content)):
                content_txt = page_content[i]["content"]
                self.show_str(content_txt, start_y + i + 2, True)
        elif "image" in page_attribute :
            image_path = page_info["content"][0]["content"]
            self.__set_background(os.path.join(self.image_path, image_path))

        elif "body" in page_attribute:
            start_y = self.__get_start_y(len(page_content))
            for i in range(0, len(page_content)):
                content_txt = page_content[i]["content"]
                self.__content_duang(content_txt, page_content[i]["attribute"], start_y + i)

        elif "code" in page_attribute :
            start_y = self.__get_start_y(len(page_content))
            max_len = 0
            max_len_index = 0
            for i in range(0, len(page_content)):
                content_txt = page_content[i]["content"]
                code_len = len(content_txt)
                for index in content_txt:
                    if self.__is_cn_char(index):
                        code_len += 1
                if code_len > max_len:
                    max_len = code_len
                    max_len_index = i
            start_x = self.__get_start_x(page_content[max_len_index]["content"])
            for i in range(0, len(page_content)):
                if "getch" in page_content[i]["attribute"]:
                    self.screen.getch()
                content_txt = page_content[i]["content"]
                self.show_code(content_txt, start_y + i, start_x, True)

    #页面特效判断
    def __page_duang_before(self, attribute):
        if "flash" in attribute:
            self.__clr()
            curses.flash()
        if "slip" in attribute:
            self.__slip_into()
        self.__clr()

    def __page_duang_after(self, attribute):
        if "printtonext" in attribute:
            height = self.height
            self.__print_with_sleep(":next page", 0, height - 1)

    def __content_duang(self, content_txt, attribute, start_y):
        if "getch" in attribute:
            self.screen.getch()
        if "image" in attribute:
            self.screen.getch()
            self.__set_background(os.path.join(self.image_path, content_txt))
            self.screen.getch()
            self.__reset_background()
            return
        if "printer" in attribute:
            self.show_str(content_txt, start_y, True)
        else:
            self.show_str(content_txt, start_y, False)

        if "flash" in attribute:
            curses.flash()

    def show_str(self, printstr, height, sleep):
        start_x = self.__get_start_x(printstr)
        if sleep == True:
            self.__print_with_sleep(printstr, start_x, height)
        else:
            self.__print_without_sleep(printstr, start_x, height)

    def show_code(self, printstr, height, start_x, sleep):
        if sleep == True:
            self.__print_with_sleep(printstr, start_x, height)
        else:
            self.__print_without_sleep(printstr, start_x, height)

    def __print_with_sleep(self, printstr, start_x, start_y):
        strlen = len(printstr)
        ch_placeholder = 0
        for i in range(0, strlen):
            self.__print_char(start_y, start_x + i + ch_placeholder, printstr[i])
            if self.__is_cn_char(printstr[i]):
                ch_placeholder += 1
            sleep(float(default_line_time) / strlen)

    def __print_without_sleep(self, printstr, start_x, start_y):
        if self.__check_out_of_screen(start_x, start_y):
            self.screen.addstr(start_y, start_x, printstr)

    def __check_out_of_screen(self, x, y):
        if x < 0 or y < 0:
            return False
        elif x >= self.width or y >= self.height:
            return False
        return True

    # page slip into the screen
    def __slip_into(self):
        width = self.width - 1
        height = self.height
        while width > 1:
            i = 0
            while i < height - 1:
                self.__print_without_sleep("▇", width, i)
                i += 1
            self.screen.refresh()
            sleep(0.001)
            width -= 1

        width = self.width - 1
        height = self.height
        while width > 1:
            i = 0
            while i < height - 1:
                self.__print_without_sleep(" ", width, i)
                i += 1
            self.screen.refresh()
            sleep(0.001)
            width -= 1

    def __clr(self):
        self.screen.clear()
        self.screen.refresh()

    def __print_char(self, y, x, char):
        if self.__check_out_of_screen(x, y):
            self.screen.addstr(y, x, char)
            self.screen.refresh()

    def __set_background(self, path):
        set_back_str = "osascript -e \'tell application \"iTerm\" to set background image path of current session of current terminal to \"" + self.currentpath + "/" +path + "\"\'"
        os.system(set_back_str)

    def __reset_background(self):
        set_back_str = "osascript -e \'tell application \"iTerm\" to set background image path of current session of current terminal to \"\"\'"
        os.system(set_back_str)

    def __is_cn_char(self, i):
            #return 0x4e00<=ord(i)<0x9fa6
            return not ord(i) < 0x3000

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
    tp = TerminalPresentation(sys.argv[1])
