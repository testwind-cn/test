# -*- coding: utf-8 -*-
"""
Created on Tue April 16 13:31:29 2023
"""
import random
import time
import tkinter as tk
import copy
from tkinter.messagebox import showinfo
from functools import partial
from tkinter.ttk import Frame


game_speed = 100

menu_frame = None

current_stage = None

record_list = []  # 记录每步的操作，供撤消用
backup_map = []  # 备份地图，供恢复用


# 000000    0 空白
# 000001    1 墙
# 001000    8 人
# 000100    4 终点
# 000010    2 箱子
# 010001   17 墙上的门
# 100000   32 机器人

try:  # 同目录下搜寻m.txt地图扩充文件，若没有此文件就用内置地图
    with open("map.txt", "r") as f:
        game_maps = f.read()
        game_maps = eval(game_maps)
except:
    game_maps = [[
        [0, 0, 1,  1, 1, 0, 0,  0],
        [0, 0, 1,  4, 1, 0, 0,  0],
        [0, 0, 1,  0, 1, 1, 1,  1],
        [1, 1, 1,  2, 0, 2, 4, 17],
        [1, 4, 2, 32, 8, 1, 1,  1],
        [1, 1, 1,  1, 2, 1, 0,  0],
        [0, 0, 0,  1, 4, 1, 0,  0],
        [0, 0, 0,  1, 1, 1, 0,  0]
    ], [
        [0,  0, 0, 1, 1, 1, 1, 1, 1,  0],
        [0,  1, 1, 1, 0, 0, 0, 0, 1,  0],
        [1,  1, 4, 0, 2, 1, 1, 0, 1,  1],
        [1,  4, 4, 2, 0, 2, 0, 0, 8, 17],
        [1, 36, 4, 0, 2, 0, 2, 0, 1,  1],
        [1,  1, 1, 1, 1, 1, 0, 0, 1,  0],
        [0,  0, 0, 0, 0, 1, 1, 1, 1,  0]
    ], [
        [0,  0, 1, 1, 1,  1, 0, 0],
        [0,  0, 1, 4, 4,  1, 0, 0],
        [0,  1, 1, 0, 4,  1, 1, 0],
        [0,  1, 0, 0, 2, 36, 1, 0],
        [1,  1, 0, 2, 0,  0, 1, 1],
        [1,  0, 0, 1, 2,  2, 0, 1],
        [1,  0, 0, 8, 0,  0, 0, 1],
        [1, 17, 1, 1, 1,  1, 1, 1]
    ], [
        [1, 17, 1, 1, 1,  1, 1, 1],
        [1,  0, 0, 1, 0,  0, 0, 1],
        [1,  0, 2, 4, 4,  2, 0, 1],
        [1,  8, 2, 4, 6, 32, 1, 1],
        [1,  0, 2, 4, 4,  2, 0, 1],
        [1,  0, 0, 1, 0,  0, 0, 1],
        [1,  1, 1, 1, 1,  1, 1, 1]
    ], [
        [0,  0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,  0],
        [0,  0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1,  0],
        [0,  0, 0, 0, 0, 1, 0, 0, 2, 2, 0, 1,  0],
        [1,  1, 1, 1, 1, 1, 0, 2, 1, 0, 0, 1,  0],
        [1, 36, 4, 4, 1, 1, 1, 0, 1, 0, 0, 1,  1],
        [1,  4, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0,  1],
        [1,  4, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 17],
        [1,  4, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0,  1],
        [1,  4, 4, 4, 1, 1, 1, 0, 1, 0, 0, 1,  1],
        [1,  1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 1,  0],
        [0,  0, 0, 0, 0, 1, 0, 8, 1, 0, 0, 1,  0],
        [0,  0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,  0],
    ], [
        [1, 17, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 32, 0, 1],
        [1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 4, 4, 4, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 6, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 8, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]]


the_dir = [
    ( 0,-1),
    ( 1, 0),
    ( 0, 1),
    (-1, 0)
]


class FramePos:
    the_map = []        # 当前地图数据，二维数组
    map_height = 0      # 地图行高度
    map_width = 0       # 地图列宽度
    door_x = 0          # 出口在地图的位置
    door_y = 0          # 出口在地图的位置
    path_w = []         # 离出口的距离权重，二维数组

    def set_path_weight(self):
        """ 计算每个单元格离出口的距离权重 """
        list_w = []                             # 二维表结果数据设为空
        for y in range(self.map_height):        # 循环每一行
            w = []                              # 新建一个空行列表
            for x in range(self.map_width):     # 循环一行的每一格
                if self.the_map[y][x] & 16:     # 如果是出门门
                    w.append(0)                 # 就添加一个0距离
                elif self.the_map[y][x] & 3:    # 如果是 1墙 和 2箱子
                    w.append(-1)                # 就添加一个 -1 距离
                else:                           # 否则
                    w.append(4096)              # 添加非常大的 4096 距离
            list_w.append(w)                    # 把这一行数据，添加到二维表的尾部
        self.path_w = list_w                    # 把赋值给 path_w

        path_weight = [(self.door_x, self.door_y, 0)]  # 路径距离计算列表，先放入出口位置，距离为0

        while len(path_weight) > 0:                     # 如果列表中有数据
            x, y, w = path_weight.pop()                 # 就从头部取一个出来：位置+距离
            for m in the_dir:                           # 循环4个方向的增量
                if 0 <= x + m[0] < self.map_width and 0 <= y + m[1] < self.map_height:
                    n = self.path_w[y + m[1]][x + m[0]]     # 获取增量位置的距离给 n
                    if n > w + 1:                           # 如果增量位置的距离 比 w+1 距离还大
                        self.path_w[y + m[1]][x + m[0]] = w + 1             # 就把 w+1 作为新距离给这个增量位置
                        path_weight.append((x + m[0], y + m[1], w + 1))     # 这个增量位置的距离变了，把它加到距离计算列表的尾部

    def find_door(self):
        """ 查找出口门的坐标 """
        for y in range(self.map_height):        # 循环地图的每一行
            for x in range(self.map_width):     # 循环当前行的每一格
                if self.the_map[y][x] & 16:     # 如果当前位置数据 并计算 10000 大于 0， 说明是出口门的位置
                    self.door_x = x             # 设置出口门横坐标
                    self.door_y = y             # 设置出口门纵坐标
                    return

    def set_map(self, a_map):
        """ 设置当前地图 """
        if isinstance(a_map, list) and len(a_map) > 0:  # 检查整体是列表，并且行数要大于0
            a = a_map[0]                                # 让 a = 第一行，应该也是
            if isinstance(a, list) and len(a) > 0:      # 检查第一行是列表，并且一行中的元素
                self.the_map = a_map                    # 确认是二维数组，就保存下来
                self.map_height = len(a_map)            # 保存地图行高度
                self.map_width = len(a)                 # 保存地图列宽度
                self.find_door()                        # 查找出口门的位置
                self.set_path_weight()                  # 计算每个位置到出口的距离
            else:
                self.__clear()                          # 否则不是正确地图，清除数据
        else:
            self.__clear()                              # 否则不是正确地图，清除数据

    def __clear(self):
        """ 清除地图数据 """
        self.the_map = []                               # 地图二维表情况
        self.path_w = []                                # 每个位置到出口距离表情况
        self.map_height = 0                             # 地图行高度为0
        self.map_width = 0                              # 地图列宽度为0
        self.door_x = 0                                 # 出口门位置x为0
        self.door_y = 0                                 # 出口门位置y为0

    def __init__(self):
        """ 初始化地图数据 """
        self.__clear()

        self.cell_size = 48                 # 方格单元格大小
        self.cell_gap = 1                   # 方格间距
        self.margin_x = 25                  # 左右边距 frame_x
        self.margin_y = 25                  # 上下边距 frame_y

        self.max_cells = 18                 # 游戏画布里，长宽最大单元格数
        self.win_w_plus = 250               # 窗口右边额外多出的宽度
        self.win_h_plus = 60                # 窗口上边额外多出的高度
        self.big_map = 0                    # 判断当前地图是否是超出窗口大小。1为是，0为不是

        self.canvas_w = 100                 # 游戏画布宽
        self.canvas_h = 100                 # 游戏画布高

        self.win_w_size = self.canvas_w + self.win_w_plus   # 窗口宽
        self.win_h_size = self.canvas_h + self.win_h_plus   # 窗口高

        self.canvas_bg = '#d7d7d7'          # 游戏背景色

        self.color_dict = {
            0: 'white',                     # 0 表示空白
            1: '#808080',                   # 1 表示墙
            8: 'yellow',                    # 8 表示空地上的人
            2: "#6CC574",                   # 2 表示空地上的箱子
            4: 'pink',                      # 4 表示终点
            6: 'red',                       # 6 表示终点上的的箱子
            12: '#ffa579',                  # 12 表示在终点上的人
            17: 'darkgreen'                 # 17 有出口门的墙
        }

    def calc_map(self):
        """ 根据地图自动调整窗口大小 """
        if isinstance(self.the_map, list) and len(self.the_map) > 0:
            a = self.the_map[0]                         # 地图是数组
            if isinstance(a, list) and len(a) > 0:
                pass                                    # 地图是二维数组
            else:                                       # 地图不是二维数组
                return
        else:                                           # 地图不是数组，退出
            return

        # 画布长宽等于= 地图行列数乘单元格大小 + 两边的空白
        self.canvas_w = self.map_width * self.cell_size + self.margin_x * 2
        self.canvas_h = self.map_height * self.cell_size + self.margin_y * 2

        # 若地图过大，窗口则使用 单元格数量 = max_cells 值来计算大小
        if self.map_width > self.max_cells:
            self.big_map = 1
            self.canvas_w = self.cell_size * self.max_cells + self.margin_x * 2
        if self.map_height > self.max_cells:
            self.big_map = 1
            self.canvas_h = self.cell_size * self.max_cells + self.margin_y * 2

        self.win_w_size = self.canvas_w + self.win_w_plus
        self.win_h_size = self.canvas_h + self.win_h_plus


# 定义一个窗口位置的全局变量
the_fp = FramePos()


class Sprite:
    """ 精灵父类 """
    def create_me(self, canvas, x=-1, y=-1):
        """ 创建自身绘图元素，画布，坐标可忽略 """
        global the_fp

        if x >= 0:          # 如果是默认 -1 就维持原来的不变，首次是0
            self.x = x
        if y >= 0:          # 如果是默认 -1 就维持原来的不变，首次是0
            self.y = y

        # 获取 自身元素 的左上、右下 坐标
        x1, y1, x2, y2 = self.get_rect()

        if self.__style == 0:                       # 如果是0，就创建正方形
            self.me = canvas.create_rectangle(
                x1 + the_fp.cell_gap,
                y1 + the_fp.cell_gap,
                x2 + the_fp.cell_gap,
                y2 + the_fp.cell_gap,
                fill=self.__color,  # "blue",
                # outline=self.canvas_bg,
                width=0)
        else:
            self.me = canvas.create_oval(
                x1 + the_fp.cell_gap,               # 如果是1，就创建圆形
                y1 + the_fp.cell_gap,
                x2 + the_fp.cell_gap,
                y2 + the_fp.cell_gap,
                fill=self.__color,  # "blue",
                # outline=self.canvas_bg,
                width=0)

    def __init__(self, color, size, style, mask):
        """ 初始化自身，传入：颜色，尺寸，类型，标志掩码"""
        self.__color = color        # 颜色
        self.__style = style        # 类型：0 方块， 1 圆形
        self.__size = size          # 尺寸：3
        self.__mask = mask          # 标志掩码：8 人， 32 机器人， 2 箱子
        self.x = 0                  # 当前位置
        self.y = 0                  # 当前位置
        self.dx = 0                 # 移动方向
        self.dy = 0                 # 移动方向
        self.me = None              # 自身绘图元素

    def position_move(self, dx, dy):
        """ x,y 增量移动 dx , dy """
        self.x += dx
        self.y += dy
        self.dx = dx
        self.dy = dy

    def position_set(self, x, y, dx=0, dy=0):
        """ 设置位置， 可以带增量移动 dx , dy """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def position_init(self):
        """ 初始化位置，在地图数据上，找到自身 """
        a_map: list = the_fp.the_map            # 全局地图数据
        for y in range(0, len(a_map)):          # 循环每一行
            for x in range(0, len(a_map[y])):   # 循环一行中的每一格
                if a_map[y][x] & self.__mask:   # 当前位置数据 和 自身的标志掩码求 并，如果大于0
                    self.x = x                  # 这就是自身位置
                    self.y = y
                    break                       # 跳出不再查找

    def del_me(self, canvas):
        """ 删除自身绘图元素 """
        if self.me is not None:                 # 自身绘图元素不是空
            canvas.delete(self.me)              # 在画布上删除元素
            self.me = None                      # 元素清空

    def draw(self, canvas):
        """ 绘画自身 """
        if self.me is None:                     # 如果自身绘图元素为空
            self.create_me(canvas)              # 创建自身绘图元素
        else:                                   # 计算自身在画布的位置
            x1 = the_fp.margin_x + the_fp.cell_size * self.x + the_fp.cell_gap + self.__size
            y1 = the_fp.margin_y + the_fp.cell_size * self.y + the_fp.cell_gap + self.__size
            canvas.moveto(self.me, x1, y1)      # 在画布上定位自身位置

    def get_rect(self):
        """ 获取 自身元素 的左上、右下 坐标 """
        x1 = the_fp.margin_x + the_fp.cell_size * self.x + the_fp.cell_gap + self.__size
        y1 = the_fp.margin_y + the_fp.cell_size * self.y + the_fp.cell_gap + self.__size
        x2 = the_fp.margin_x + the_fp.cell_size * (self.x + 1) - 2 * the_fp.cell_gap - self.__size
        y2 = the_fp.margin_y + the_fp.cell_size * (self.y + 1) - 2 * the_fp.cell_gap - self.__size
        return x1, y1, x2, y2

    def same_position(self, x, y):
        """ 自己的坐标和x,y进行比较，是否相等"""
        if self.x == x and self.y == y:
            return True
        else:
            return False

    def process_key(self, event):
        """ 检查方向键、空格键，根据按键，返回x,y的变化值"""
        key = event.keysym

        if key == 'Up' or key == 'W' or key == 'w':
            return True, 0, -1
        elif key == 'Down' or key == 'S' or key == 's':
            return True, 0, 1
        elif key == 'Left' or key == 'A' or key == 'a':
            return True, -1, 0
        elif key == 'Right' or key == 'D' or key == 'd':
            return True, 1, 0
        elif key == 'space':
            return True, 0, 0
        else:
            return False, 0, 0


class Robot(Sprite):
    """ 机器人，继承精灵父类 """

    def __init__(self, color="#556633", size=10):
        """ 构造函数，默认颜色，默认尺寸10，调用父类构造，标志掩码 32 """
        super().__init__(color, size, 1, 32)
        self.wait_max = 2                       # 延时减速周期2
        self.wait = 0                           # 第0次延时计数器
        self.dir = 0                            # 当前移动朝向序号， 0,1,2,3

    def process_ai(self):
        if self.wait < self.wait_max:           # 还没到延时减速周期
            self.wait += 1                      # 增加一次延时计数器
            return False                        # 返回否，表示没有移动
        else:
            self.wait = 0                       # 达到延时周期，延时计数器归零

        delta = random.Random().randint(0, 1)*2 - 1   # 随机数 +1 或 -1， 用来方向变大或变小

        for m in range(4):                      # m 从 0 循环到 3
            s = (self.dir + 4 + delta * m) % 4  # 调整dir值，根据delta正负，dir依次加0到3， 或者依次减0到3
            x1 = self.x + the_dir[s][0]         # 得到增量位置的 x1 , y1
            y1 = self.y + the_dir[s][1]

            # 如果这个增量位置在地图里，没有越界
            if 0 <= x1 < the_fp.map_width and 0 <= y1 < the_fp.map_height:
                n1 = the_fp.path_w[self.y][self.x]  # 原来位置到出口的距离
                n2 = the_fp.path_w[y1][x1]          # 增量位置到出口的距离
                if 0 <= n2 < n1:                    # 如果新位置比原位置的距离小，并且不是-1墙
                    self.y = y1                     # 使用这个新位置
                    self.x = x1
                    self.dir = s                    # 使用这个新的方向，值是 0,1,2,3
                    return True                     # 移动了，返回真

        for m in range(4):                          # 上面没有移动，再扫描4次，可以接受距离不变的移动，进行乱逛
            s = (self.dir + 4 + delta * m) % 4
            x1 = self.x + the_dir[s][0]
            y1 = self.y + the_dir[s][1]

            if 0 <= x1 < the_fp.map_width and 0 <= y1 < the_fp.map_height:
                n1 = the_fp.path_w[self.y][self.x]
                n2 = the_fp.path_w[y1][x1]
                if 0 <= n2 <= n1:                   # 如果新位置距离小于等于原位置
                    self.y = y1                     # 更新到这个位置
                    self.x = x1
                    self.dir = s
                    return True

        return False                                # 没有移动，返回否


class Worker(Sprite):
    """ 搬运工类，继承精灵父类 """
    def create_me(self, canvas, x=-1, y=-1):
        """ 创建自身，调用父类，再多创建两个椭圆 """
        super().create_me(canvas)

        # 获取左上，右下坐标
        x1, y1, x2, y2 = self.get_rect()

        # 创建两个椭圆
        self.me1 = canvas.create_oval(x1-8, y1+10, x2+8, y2-10, outline="red", width=2)
        self.me2 = canvas.create_oval(x1+10, y1-8, x2-10, y2+8, outline="red", width=2)

        self.__draw_dagger(canvas)      # 重绘两个拖钩

        # filename = tk.PhotoImage(file ="aa.gif")
        # self.me = canvas.create_image(50,50,image=filename)

    def __init__(self, color="blue", size=6, style=1):
        """ 构建函数，蓝色，尺寸6，类型方框 """
        super().__init__(color, size, style, 8)
        self.me1 = None                 # 椭圆1为空
        self.me2 = None                 # 椭圆2为空
        self.drag = False               # 拖动状态为否

    def del_me(self, canvas):
        """ 删除自身图像元素 """
        super().del_me(canvas)
        # 调用父类删除自身，再删除两个椭圆
        if self.me1 is not None:
            canvas.delete(self.me1)
            self.me1 = None
        if self.me2 is not None:
            canvas.delete(self.me2)
            self.me2 = None

    def __draw_dagger(self, canvas):
        """ 绘画两个椭圆拖钩 """
        if self.me1 is not None and self.me2 is not None:
            x1, y1, x2, y2 = self.get_rect()        # 如果两个椭圆元素不是空，获取自身左上右下坐标
            canvas.moveto(self.me1, x1-8, y1+10)    # 把两个椭圆移动到当前位置
            canvas.moveto(self.me2, x1+10, y1-8)
            if self.drag:           # 如果拖动状态是真，就在画布上显示正常
                canvas.itemconfig(self.me1, state="normal")
                canvas.itemconfig(self.me2, state="normal")
            else:                   # 如果拖动状态是否，就在画布上显示隐藏
                canvas.itemconfig(self.me1, state="hidden")
                canvas.itemconfig(self.me2, state="hidden")

    def toggle_drag(self, canvas):
        """ 切换拖钩状态 """
        self.drag = not self.drag       # 把拖钩状态真假颠倒
        self.__draw_dagger(canvas)      # 重绘拖钩

    def set_drag(self, drag):
        """ 设置拖钩状态 """
        self.drag = drag

    def draw(self, canvas):
        """ 先绘画自身，再绘画拖钩 """
        super().draw(canvas)
        self.__draw_dagger(canvas)


class Box(Sprite):
    """ 箱子类， 继承精灵父类"""

    def __init__(self, color="#6C3E22", size=3, style=0):
        """ 初始化默认颜色，尺寸3，类型是方框，标志掩码是2 """
        super().__init__(color, size, style, 2)


class PlayFrame:
    def __init__(self, win, game_stage):
        global main_win

        self.exitKeyTime = 0

        self.canvas_map = []
        self.canvas_worker = None
        self.canvas_boxes = []

        self.record_list = []

        self.robots = []        # 多个机器人

        self.stage = 1

        self.frame: Frame = None
        self.canvas: tk.Canvas = None

        if win is None:
            return
        self.delete()

        self.frame = Frame(win, padding=(5, 20, 10, 10))  # 界面1

        frame1 = Frame(self.frame, width=400)

        self.msg_label = tk.Label(frame1, text="",
                                  font=('Arial', 11), anchor="ne", justify="left", width=20)
        self.msg_label.pack(side='left', anchor="nw")

        b = tk.Button(
            frame1,
            text="退出",
            font=('Arial', 11),
            width=10, height=1,
            command=self.exit
        )
        b.pack(side="right", anchor="ne")

        frame1.pack(side="top")

        self.canvas = tk.Canvas(self.frame,
                                bg=the_fp.canvas_bg,
                                height=10,
                                width=10,
                                highlightthickness=0)

        self.canvas.pack(side='left')

        self.txt_label = tk.Label(self.frame, text="",
                                  font=('Arial', 11),
                                  # anchor="ne",
                                  justify="left", width=30, background="lightgray",
                                  # 设置填充区距离、边框宽度和其样式（凹陷式）
                                  padx=3, pady=3, borderwidth=3,
                                  relief="sunken")
        self.txt_label.pack(side='right')

        self.worker = Worker()

        self.robots.append(Robot())
        self.robots.append(Robot("red", 12))

    def reconfig(self, stage):
        global game_maps

        if self.msg_label is not None:
            self.msg_label.config(text="机器人解救中...")

        if self.txt_label is not None:
            self.txt_label.config(text=
                                  """ --  当前为第 {} 关 ---

 蓝色单元格为工人
 绿色圆圈是机器人
 
 白色单元格为空地
 灰色单元格为墙
 粉色单元格为终点
 
 褐色单元格为箱子
 红边框褐色格为到终点的箱子

 上下左右方向键移动
 字母键B为撤消
 
 【空格】打开/关闭拖钩
 有红色拖钩时，可以拖背后箱子

 连按两下Esc, 返回主页面
 
 数字键1~6直接选择关卡
 （第六关为测试关）
""".format(str(self.stage+1)))

        # 根据地图自动调整窗口大小

        self.stage = stage
        map = copy.deepcopy(game_maps[stage])
        the_fp.set_map(map)
        the_fp.calc_map()

        if self.canvas is not None:
            self.canvas.config(
                bg=the_fp.canvas_bg,
                width=the_fp.canvas_w,
                height=the_fp.canvas_h)
            self.worker.del_me(self.canvas)
            for rob in self.robots:
                rob.del_me(self.canvas)
            self.canvas.delete("all")
            self.create_game_cells()

        main_win.window_center("操作", the_fp.win_w_size, the_fp.win_h_size)

        self.worker.position_init()
        self.worker.drag = True
        self.worker.toggle_drag(self.canvas)
        self.worker.draw(self.canvas)
        for rob in self.robots:
            rob.position_init()
            rob.draw(self.canvas)

        if len(self.canvas_boxes) > 0:
            for box in self.canvas_boxes:
                self.canvas.delete(box.me)
            # for i in range(0,len(self.canvas_boxes)):
            #    self.canvas.delete(self.canvas_boxes[i])

        self.canvas_boxes = []
        for y in range(0, the_fp.map_height):
            for x in range(0, the_fp.map_width):
                if (the_fp.the_map[y][x] & 2) > 0 : # 并且上10 箱子
                    box = Box()
                    box.create_me(self.canvas, x, y)
                    self.canvas_boxes.append(box)

    def create_game_cells(self):
        if self.canvas is None:
            return
        # 如果是大地图，更换起始坐标，以人物为中心建立地图
        map_x = the_fp.map_width
        map_y = the_fp.map_height

        if the_fp.big_map == 1:
            if self.worker.x > int(the_fp.max_cells // 2):
                if self.worker.x < map_x - int(the_fp.max_cells // 2):
                    px = self.worker.x - int(the_fp.max_cells // 2)
                elif self.worker.x >= map_x - int(the_fp.max_cells // 2):
                    px = map_x - the_fp.max_cells
            else:
                px = 0

            if self.worker.y > int(the_fp.max_cells // 2):
                if self.worker.y < map_y - int(the_fp.max_cells // 2):
                    py = self.worker.y - int(the_fp.max_cells // 2)
                elif self.worker.y >= map_y - int(the_fp.max_cells // 2):
                    py = map_y - the_fp.max_cells
            else:
                py = 0
        else:
            px = 0
            py = 0

        py = 0
        px = 0
        self.canvas_map = []

        for y in range(0, the_fp.map_height - py):
            rect_list = []
            for x in range(0, the_fp.map_width - px):
                a_rect = self.canvas.create_rectangle(
                    the_fp.margin_x + the_fp.cell_size * x + the_fp.cell_gap,
                    the_fp.margin_y + the_fp.cell_size * y + the_fp.cell_gap,
                    the_fp.margin_x + the_fp.cell_size * (x + 1),
                    the_fp.margin_y + the_fp.cell_size * (y + 1),
                                             fill=the_fp.color_dict[the_fp.the_map[y + py][x + px] & (~32)],
                                             outline=the_fp.canvas_bg,
                                             width=0)
                rect_list.append(a_rect)
            self.canvas_map.append(rect_list)

        # self.canvas.place(x=0,y=0)

    def redaw_game_cells(self):
        if self.canvas is None:
            return

        if self.canvas_map is None or len(self.canvas_map) <= 0:
            return

        for y in range(0, the_fp.map_height):
            if len(self.canvas_map) <= y:
                return
            rect_list = self.canvas_map[y]
            if rect_list is None or len(rect_list) <= 0:
                return

            for x in range(0, the_fp.map_width):
                if len(rect_list) <= x:
                    return

                self.canvas.itemconfig(rect_list[x], fill=the_fp.color_dict[the_fp.the_map[y][x] & (~32)])

    def delete(self):
        if self.canvas is not None:
            self.canvas.pack_forget()
            self.canvas.destroy()
            del self.canvas
            self.canvas = None

        if self.frame is not None:
            self.frame.pack_forget()
            self.frame.destroy()
            del self.frame
            self.frame = None

    def __del__(self):
        return

    def show(self, visible: bool):
        if self.frame is not None:
            if visible:
                self.frame.pack()
            else:
                self.frame.pack_forget()

    def history_restore(self):
        if len(self.record_list) <= 0:
            return

        temp = self.record_list.pop()

        the_fp.the_map[self.worker.y][self.worker.x] &= 7  # & 0111 去掉人

        self.worker.position_set(temp[0], temp[1], temp[2], temp[3])
        self.worker.set_drag(temp[4] == 1)
        dx = temp[5]
        dy = temp[6]
        the_fp.the_map[self.worker.y + dy + 0][self.worker.x + dx + 0] = temp[7]
        the_fp.the_map[self.worker.y + dy - 1][self.worker.x + dx + 0] = temp[8]
        the_fp.the_map[self.worker.y + dy + 1][self.worker.x + dx + 0] = temp[9]
        the_fp.the_map[self.worker.y + dy + 0][self.worker.x + dx - 1] = temp[10]
        the_fp.the_map[self.worker.y + dy + 0][self.worker.x + dx + 1] = temp[11]

        the_fp.the_map[self.worker.y - dy][self.worker.x - dx] = temp[12]

        i = 13
        for box in self.canvas_boxes:
            box.position_set(temp[i], temp[i+1])
            i += 2

    def history_save(self, dx, dy):
        temp = []                       # 记录每步的操作，供撤消使用。
        temp.append(self.worker.x)      # 保存XY轴坐标值，即人物所在单元格的坐标
        temp.append(self.worker.y)      # 后面6个分别是中，上，下，左，右  和 背后拖出来单元格的值
        temp.append(self.worker.dx)     # 角色原来朝向
        temp.append(self.worker.dy)     # 角色原来朝向
        temp.append(1 if self.worker.drag else 0)    # 角色原来是否拖动模式
        temp.append(dx)             # 角色新移动朝向
        temp.append(dy)             # 角色新移动朝向
        temp.append(the_fp.the_map[self.worker.y + dy + 0][self.worker.x + dx + 0])
        temp.append(the_fp.the_map[self.worker.y + dy - 1][self.worker.x + dx + 0])
        temp.append(the_fp.the_map[self.worker.y + dy + 1][self.worker.x + dx + 0])
        temp.append(the_fp.the_map[self.worker.y + dy + 0][self.worker.x + dx - 1])
        temp.append(the_fp.the_map[self.worker.y + dy + 0][self.worker.x + dx + 1])

        temp.append(the_fp.the_map[self.worker.y - dy][self.worker.x - dx])

        for box in self.canvas_boxes:
            temp.append(box.x)
            temp.append(box.y)

        self.record_list.append(temp)

        if len(self.record_list) > 1:
            if self.record_list[-1] == self.record_list[-2]:
                del self.record_list[-1]  # 删除连续相同的数据

    def process_key_menu(self, event):
        if '1' <= event.keysym <= '6':
            res = tk.messagebox.askokcancel("确认", "是否切换到第 {} 关".format(int(event.keysym)))
            if res:
                main_win.change(int(event.keysym) - 1)
            return False

        if event.keysym == 'b':
            self.history_restore()
            self.worker.draw(self.canvas)
            for rob in self.robots:
                rob.draw(self.canvas)
            return True

        if event.keysym == 'Escape':  # 处理退出按键
            new_time = time.time()
            if new_time < self.exitKeyTime + 5:  # 5秒内，第二次按键，退出
                self.exitKeyTime = 0
                if self.msg_label is not None:
                    self.msg_label.config(text="机器人解救中...")
                main_win.change()
            else:  # 第一次按键
                self.exitKeyTime = new_time
                if self.msg_label is not None:
                    self.msg_label.config(text="再次按 <ESC> 退出...")

        return False

    def process_key_boy(self, event):
        res, dx, dy = self.worker.process_key(event)

        if (dx == 0) and (dy == 0) and res:         # 玩家没有动, 按了空格
            self.worker.toggle_drag(self.canvas)
            self.worker.draw(self.canvas)
            return False

        if not res:     # 玩家没有动
            return False

        # 玩家移动了
        face_item = the_fp.the_map[self.worker.y + dy][self.worker.x + dx]
        back_item = the_fp.the_map[self.worker.y - dy][self.worker.x - dx]
        #  1 0001 墙
        # 12 1100 人+终点
        #  8 1000 人+空地

        res = False

        if face_item & 1 or face_item & 8:    # 前面是墙或者人，返回。 1 墙， 8 人
            return False

        if face_item & 2 <= 0:              # 前方没有东西 , 没有箱子，已经没有墙，可以走过去    # 0 空地 # 4  100 终点，

            no_rob = True                                               # 工人位置没有机器人
            for rob in self.robots:
                if rob.same_position(self.worker.x, self.worker.y):
                    no_rob = False                                      # 工人位置有机器人
                    break

            if self.worker.drag and back_item & 2 and no_rob:            # 背后有箱子, 并且机器人不在这里
                self.history_save(dx, dy)
                res = True

            # 拉动背后箱子
            if self.worker.drag and back_item & 2 and no_rob:                           # 当前位：工人背后有箱子, 工人位没有机器人
                the_fp.the_map[self.worker.y - dy][self.worker.x - dx] &= (~2)     # 背后位：拖走箱子， 去掉  0010
                the_fp.the_map[self.worker.y][self.worker.x] |= 2                  # 当前位：拖来箱子，加上  0010
                for box in self.canvas_boxes:                                           # 背后位：拖走箱子
                    if box.same_position(self.worker.x - dx, self.worker.y - dy):
                        box.position_move(dx, dy)
                        break

            the_fp.the_map[self.worker.y + dy][self.worker.x + dx] |= 8    # 前面位：走来一个人     = 8  加上人
            the_fp.the_map[self.worker.y][self.worker.x] &= (~8)           # 当前位：离开一个人     & 11110111 原来位置去掉人

            self.worker.position_move(dx, dy)


        else:               # new_item == 2 or new_item == 6:           # 前面有箱子     2   010 箱子+空地  # 6  110 已经完成

            next_item = the_fp.the_map[self.worker.y + 2 * dy][self.worker.x + 2 * dx]
            # 推的箱子的再前面没有箱子  11 没有墙+箱子
            no_rob = True                                               # 推的箱子的再前面位置没有机器人
            for rob in self.robots:
                if rob.same_position(self.worker.x + 2 * dx, self.worker.y + 2 * dy):
                    no_rob = False                                      # 推的箱子的再前面位置没有机器人
                    break

            if next_item & 3 == 0 and no_rob:                            # 推的箱子再前面: 没有箱子，没有墙，没有机器人
                self.history_save(dx, dy)
                res = True

                for box in self.canvas_boxes:                                               # 推动一个箱子位置调整
                    if box.same_position(self.worker.x + dx, self.worker.y + dy):
                        box.position_move(dx, dy)
                        break

                no_rob = True                                                               # 当前位：工人位置没有机器人
                for rob in self.robots:
                    if rob.same_position(self.worker.x, self.worker.y):
                        no_rob = False                                                      # 当前位：工人位置有机器人
                        break

                # 拉动背后箱子
                if self.worker.drag and back_item & 2 and no_rob:                           # 当前位：工人背后有箱子, 工人位没有机器人
                    the_fp.the_map[self.worker.y - dy][self.worker.x - dx] &= (~2)     # 背后位：拖走箱子， 去掉  0010
                    the_fp.the_map[self.worker.y][self.worker.x] |= 2                  # 当前位：拖来箱子，加上  0010
                    for box in self.canvas_boxes:                                           # 背后位：拖走箱子
                        if box.same_position(self.worker.x - dx, self.worker.y - dy):
                            box.position_move(dx, dy)
                            break

                the_fp.the_map[self.worker.y + dy][self.worker.x + dx] |= 8            # 前面位：走来一个人     = 8  加上人
                the_fp.the_map[self.worker.y][self.worker.x] &= (~8)                   # 当前位：离开一个人     & 11110111 原来位置去掉人

                the_fp.the_map[self.worker.y + 2 * dy][self.worker.x + 2 * dx] |= 2    # 再前面：推来一个箱子    或者上10 箱子
                the_fp.the_map[self.worker.y + dy][self.worker.x + dx] &= (~2)         # 前面位：推走一个箱子去掉 1101 箱子

                self.worker.position_move(dx, dy)

        # self.worker.draw(self.canvas)
        self.redraw()
        return res

    def process_key(self, event):
        print(" In game " + event.keysym)

        res = self.process_key_menu(event)

        if res:
            return res

        res = self.process_key_boy(event)

        if res:
            the_fp.set_path_weight()
            self.check_game_pass()

        return res

    def update_clock(self):

        if self.exitKeyTime > 0:
            newtime = time.time()
            if newtime >= self.exitKeyTime + 5:  # 超过5秒，恢复操作
                self.exitKeyTime = 0
                if self.msg_label is not None:
                    self.msg_label.config(text="机器人解救中...")

        pass
        # 123

    def process_ai(self):
        res = False
        for rob in self.robots:
            res = res or rob.process_ai()
        if res:
            for rob in self.robots:
                rob.draw(self.canvas)
            self.check_game_pass2()
        pass
        # self.check_game_pass()

    def check_game_pass(self):  # 通关条件为箱子数为0
        """ 获取箱子数量，等于0的话过关 """
        cnt = 0
        for box in self.canvas_boxes:
            if the_fp.the_map[box.y][box.x] & 4:
                cnt += 1
        if cnt == len(self.canvas_boxes):
            self.redaw_game_cells()
            for box in self.canvas_boxes:
                box.draw(self.canvas)
            self.worker.draw(self.canvas)
            for rob in self.robots:
                rob.draw(self.canvas)
            self.pass_win()

    def pass_win(self):
        """ 箱子为零时，显示过关窗口 """
        res = tk.messagebox.askokcancel("推箱完成", "机器人未解救，是否退出")
        if res:
            main_win.change(-1)

    def check_game_pass2(self):  # 通关条件为箱子数为0
        res = True
        for rob in self.robots:
            if the_fp.the_map[rob.y][rob.x] & 16:
                pass
            else:
                res = False
                break
        if res:
            self.pass_win2()

    def pass_win2(self):
        """ 箱子为零时，显示过关窗口 """
        res = tk.messagebox.showinfo("确认", "机器人顺利解救")
        if res:
            main_win.change(-1)

    def exit(self):
        """ 箱子为零时，显示过关窗口 """
        res = tk.messagebox.askokcancel("确认","是否退出")
        if res:
            main_win.change(-1)



    def redraw(self):
        self.redaw_game_cells()
        self.worker.draw(self.canvas)
        for box in self.canvas_boxes:
            box.draw(self.canvas)
        self.worker.draw(self.canvas)
        for rob in self.robots:
            rob.draw(self.canvas)


class MainWindow:

    def __init__(self):

        self.in_menu = True
        self.fps_count = 0

        self.win = tk.Tk()
        self.menu_frame: Frame = None
        self.create_menu()
        self.play_frame: PlayFrame = PlayFrame(self.win, 1)

        self.window_center('Welcome 欢迎', 300, (len(game_maps) + 1) * 30)

    def window_center(self, title, w_size, h_size):
        self.win.focus_force()
        self.win.title(title)
        """ 窗口居中 """
        screenWidth = self.win.winfo_screenwidth()  # 获取显示区域的宽度
        screenHeight = self.win.winfo_screenheight()  # 获取显示区域的高度
        left = (screenWidth - w_size) // 2
        top = (screenHeight - h_size) // 2
        self.win.geometry("%dx%d+%d+%d" % (w_size, h_size, left, top))

    def create_menu(self):
        if self.win is None:
            return
        if self.menu_frame is not None:
            self.menu_frame.pack_forget()
            self.menu_frame.destroy()
            del self.menu_frame
            self.menu_frame = None

        self.menu_frame = Frame(self.win, padding=(5, 20, 10, 10))  # 界面1
        self.menu_frame.pack()

        for i in range(0, len(game_maps)):  # 批量添加按键
            b = tk.Button(
                self.menu_frame,
                text="进入第 " + str(i+1) + " 关",
                font=('Arial', 11),
                width=10, height=1,
                # command=self.change  # partial(to_game, i)
                command=partial(self.change, i)
            )
            b.pack()

    def change(self, to_stage=-2):
        # -1 菜单,  0-10 关卡, -2 切换
        if self.in_menu:
            self.menu_frame.pack_forget()
        else:
            self.play_frame.show(False)

        if to_stage <= -2:
            self.in_menu = not self.in_menu
            if self.in_menu:
                self.menu_frame.pack()
            else:
                self.play_frame.reconfig(to_stage)
                self.play_frame.show(True)
            return

        if to_stage == -1:
            self.in_menu = True
            self.menu_frame.pack()
        else:
            self.in_menu = False
            self.play_frame.reconfig(to_stage)
            self.play_frame.show(True)

    def show(self):
        if self.win is None:
            return

        self.win.bind('<Key>', self.key_action)
        self.win.after(1000, self.update_clock)
        self.win.mainloop()

    def check_menu_key(self, event):
        if '1' <= event.keysym <= '6':
            main_win.change(int(event.keysym) - 1)
        return False

    def update_clock(self):

        if self.fps_count >= 4:
            self.fps_count = 0
            # aa = time.time()
            # now = time.strftime("%H:%M:%S", time.localtime(aa))
            # print(now)
        else:
            self.fps_count += 1

        if not self.in_menu:
            self.play_frame.process_ai()

        self.win.after(game_speed, self.update_clock)
        if not self.in_menu:
            self.play_frame.update_clock()

    def key_action(self, event):
        """ 按键控制 """
        if self.in_menu:
            self.check_menu_key(event)
        elif self.play_frame is not None:
            res = self.play_frame.process_key(event)
            if res:
                self.play_frame.redraw()


main_win = MainWindow()

if __name__ == '__main__':
    main_win.show()
