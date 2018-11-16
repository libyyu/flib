# -*- coding: utf-8 -*-
'''
#----------------------------------------------------------------------------------------
# 功能：提供修改控制台终端颜色的接口
#----------------------------------------------------------------------------------------
'''
import sys, os
import platform
isJenkinsMode = "WINSW_EXECUTABLE" in os.environ
#print "isJenkinsMode: ", isJenkinsMode
if platform.system() == "Windows" and not isJenkinsMode:
    import ctypes
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    # 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
    # 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

    # Windows CMD命令行 字体颜色定义 text colors
    FOREGROUND_BLACK = 0x00  # black.
    FOREGROUND_DARKBLUE = 0x01  # dark blue.
    FOREGROUND_DARKGREEN = 0x02  # dark green.
    FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
    FOREGROUND_DARKRED = 0x04  # dark red.
    FOREGROUND_DARKPINK = 0x05  # dark pink.
    FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
    FOREGROUND_DARKWHITE = 0x07  # dark white.
    FOREGROUND_DARKGRAY = 0x08  # dark gray.
    FOREGROUND_BLUE = 0x09  # blue.
    FOREGROUND_GREEN = 0x0a  # green.
    FOREGROUND_SKYBLUE = 0x0b  # skyblue.
    FOREGROUND_RED = 0x0c  # red.
    FOREGROUND_PINK = 0x0d  # pink.
    FOREGROUND_YELLOW = 0x0e  # yellow.
    FOREGROUND_WHITE = 0x0f  # white.

    # Windows CMD命令行 背景颜色定义 background colors
    BACKGROUND_BLUE = 0x10  # dark blue.
    BACKGROUND_GREEN = 0x20  # dark green.
    BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
    BACKGROUND_DARKRED = 0x40  # dark red.
    BACKGROUND_DARKPINK = 0x50  # dark pink.
    BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
    BACKGROUND_DARKWHITE = 0x70  # dark white.
    BACKGROUND_DARKGRAY = 0x80  # dark gray.
    BACKGROUND_BLUE = 0x90  # blue.
    BACKGROUND_GREEN = 0xa0  # green.
    BACKGROUND_SKYBLUE = 0xb0  # skyblue.
    BACKGROUND_RED = 0xc0  # red.
    BACKGROUND_PINK = 0xd0  # pink.
    BACKGROUND_YELLOW = 0xe0  # yellow.
    BACKGROUND_WHITE = 0xf0  # white.

    STYLE = {
        'fore':
            {  # 前景色
                'black': 0x00,  # 黑色
                'red': 0x0c,  # 红色
                'green': 0x0a,  # 绿色
                'yellow': 0x0e,  # 黄色
                'blue': 0x09,  # 蓝色
                'purple': 0x0d,  # 紫红色
                'cyan': 0x03,  # 青蓝色
                'white': 0x0f,  # 白色
            },

        'back':
            {  # 背景
                'black': 0x00,  # 黑色
                'red': 0xc0,  # 红色
                'green': 0xa0,  # 绿色
                'yellow': 0xe0,  # 黄色
                'blue': 0x90,  # 蓝色
                'purple': 0xd0,  # 紫红色
                'cyan': 0x30,  # 青蓝色
                'white': 0xf0,  # 白色
            },

        'mode':
            {  # 显示模式
                'mormal': 0,  # 终端默认设置
                'bold': 1,  # 高亮显示
                'underline': 4,  # 使用下划线
                'blink': 5,  # 闪烁
                'invert': 7,  # 反白显示
                'hide': 8,  # 不可见
            },

        'default':
            {
                'end': 0,
            },
    }

    # get handle
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool


    # reset white
    def reset_cmd_color():
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
else:
    # 格式：\033[显示方式;前景色;背景色m
    #   说明:
    #
    #   前景色            背景色            颜色
    #   ---------------------------------------
    #     30                40              黑色
    #     31                41              红色
    #     32                42              绿色
    #     33                43              黃色
    #     34                44              蓝色
    #     35                45              紫红色
    #     36                46              青蓝色
    #     37                47              白色
    #
    #   显示方式           意义
    #   -------------------------
    #      0           终端默认设置
    #      1             高亮显示
    #      4            使用下划线
    #      5              闪烁
    #      7             反白显示
    #      8              不可见
    #
    #   例子：
    #   \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
    #   \033[0m          <!--采用终端默认设置，即取消颜色设置-->]]]

    STYLE = {
        'fore':
            {  # 前景色
                'black': 30,  # 黑色
                'red': 31,  # 红色
                'green': 32,  # 绿色
                'yellow': 33,  # 黄色
                'blue': 34,  # 蓝色
                'purple': 35,  # 紫红色
                'cyan': 36,  # 青蓝色
                'white': 37,  # 白色
            },

        'back':
            {  # 背景
                'black': 40,  # 黑色
                'red': 41,  # 红色
                'green': 42,  # 绿色
                'yellow': 43,  # 黄色
                'blue': 44,  # 蓝色
                'purple': 45,  # 紫红色
                'cyan': 46,  # 青蓝色
                'white': 47,  # 白色
            },

        'mode':
            {  # 显示模式
                'mormal': 0,  # 终端默认设置
                'bold': 1,  # 高亮显示
                'underline': 4,  # 使用下划线
                'blink': 5,  # 闪烁
                'invert': 7,  # 反白显示
                'hide': 8,  # 不可见
            },

        'default':
            {
                'end': 0,
            },
    }

    def UseStyle(string, mode = '', fore = '', back = ''):

        mode  = '%s' % STYLE['mode'][mode] if STYLE['mode'].has_key(mode) else ''

        fore  = '%s' % STYLE['fore'][fore] if STYLE['fore'].has_key(fore) else ''

        back  = '%s' % STYLE['back'][back] if STYLE['back'].has_key(back) else ''

        style = ';'.join([s for s in [mode, fore, back] if s])

        style = '\033[%sm' % style if style else ''

        end   = '\033[%sm' % STYLE['default']['end'] if style else ''

        return '%s%s%s' % (style, string, end)
##############################################################

def print_with_color(text, newLine=True, color=None):
    if not color:
        sys.stdout.write(text)
        if newLine: sys.stdout.write('\n')
        sys.stdout.flush()
        return
    if platform.system() == "Windows" and not isJenkinsMode:
        if color in STYLE['fore'].keys():
            set_cmd_text_color(STYLE['fore'][color])
            sys.stdout.write(text)
            if newLine: sys.stdout.write('\n')
            sys.stdout.flush()
            reset_cmd_color()
        else:
            sys.stdout.write(text)
            if newLine: sys.stdout.write('\n')
            sys.stdout.flush()
    else:
        text = UseStyle(text, fore=color)
        sys.stdout.write(text)
        if newLine: sys.stdout.write('\n')
        sys.stdout.flush()