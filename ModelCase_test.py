from cmath import sqrt
from dis import Instruction
from doctest import FAIL_FAST
from re import T
from xml.dom.minidom import Element

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime
import sys
import random
from tkinter import *
from tkinter import messagebox


class Cell(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name, ix, iy,
                 is_blocked):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)
        self.set_name(f"({ix}, {iy})")
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.ix = ix
        self.iy = iy

        self.set_blocked(is_blocked)  # True = 장애물 , 장애물 인지 아닌지 set
        # def set_blocked 는 definition.py 에 있음

        self.insert_input_port("east")
        self.insert_input_port("west")
        self.insert_input_port("north")
        self.insert_input_port("south")

        self.insert_output_port("east")
        self.insert_output_port("west")
        self.insert_output_port("north")
        self.insert_output_port("south")
        #self.cm_list = []

    def ext_trans(self, port, msg):
        # if port == "east":
        print(f"[{self.ix}, {self.iy}][IN]: {datetime.datetime.now()}")
        self.cancel_rescheduling()
        data = msg.retrieve()

        self.agent = data[0]

        self.cm_list = self.agent.get_instruction()

        print(f"Current Location:{self.get_name()}")
        print("instruction list : ", self.cm_list)

        self._cur_state = "MOVE"

    def output(self):

        if (self.get_blocked() == True):
            self.agent.ifMove()
            print(f"***The current cell[{self.get_name()}] is blocked.***")
            flag = self.agent.get_flag()
            if flag == 'rb':
                msg = SysMessage(self.get_name(), "west")
            elif flag == 'lb':
                msg = SysMessage(self.get_name(), "east")
            elif flag == 'fb':
                msg = SysMessage(self.get_name(), "south")
            elif flag == 'bb':
                msg = SysMessage(self.get_name(), "north")

        else:    
            cm = self.cm_list.pop(0)
            print(f"[{self.ix}, {self.iy}][OUT]: {datetime.datetime.now()}")

            if cm == "R":
                msg = SysMessage(self.get_name(), "east")
                self.agent.set_flag('rb')

            elif cm == "F":
                msg = SysMessage(self.get_name(), "north")
                self.agent.set_flag('fb')

            elif cm == "L":
                msg = SysMessage(self.get_name(), "west")
                self.agent.set_flag('lb')

            elif cm == "B":
                msg = SysMessage(self.get_name(), "south")
                self.agent.set_flag('bb')

        msg.insert(self.agent)
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"


class str_to_instruction():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.cm_list = list()

    def MoveR(self):
        self.cm_list.insert(0, 'R')

    def MoveL(self):
        self.cm_list.insert(0, 'L')

    def MoveF(self):
        self.cm_list.insert(0, 'F')

    def MoveB(self):
        self.cm_list.insert(0, 'B')

    def get_instruction(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.cm_list


class Agent():

    def __init__(self):
        self.cm_s = ''
        
        self.set_rbMove = None
        self.set_lbMove = None
        self.set_fbMove = None
        self.set_bbMove = None

        self.cm_list = []
        self.flag = ''

    def set_ifMove(self, block, move):
        if block == 'rb':
            self.set_rbMove = move
        elif block == 'lb':
            self.set_lbMove = move
        elif block == 'fb':
            self.set_fbMove = move
        elif block == 'bb':
            self.set_bbMove = move

    def ifMove(self):
        if self.flag == 'rb':
            if self.set_rbMove == None:
                return
            exec(self.set_rbMove)
        elif self.flag == 'lb':
            if self.set_lbMove == None:
                return
            exec(self.set_lbMove)
        elif self.flag == 'fb':
            if self.set_fbMove == None:
                return
            exec(self.set_fbMove)
        elif self.flag == 'bb':
            if self.set_bbMove == None:
                return None
            exec(self.set_bbMove)

    def list_of_instruction(self, s):
        self.cm_s = s

    def get_instruction(self):  # 만들어진 명령어 리스트를 반환한다.
        self.cm_list = self.cm_s.get_instruction()
        return self.cm_list

    def set_flag(self, flag):
        self.flag = flag
    
    def get_flag(self):
        return self.flag


# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("start")

width = 100
height = 100

mat = list()
simple_map = list()
for i in range(height):
    col = list()
    map_col = list()
    for j in range(width):
        if i == 0 and j == 0:  # 시작점은 장애물 x
            c = Cell(0, Infinite, "", "sname", j, i, False)
            map_col.append(0)
        elif i == 0 and j == 1:
            c = Cell(0, Infinite, "", "sname", j, i, True)
            map_col.append(1)
        else:
            b = random.choice([True, False, False])
            c = Cell(0, Infinite, "", "sname", j, i,
                     b)  # 랜덤으로 장애물 생성  True = 장애물
            if (b == True):  #장애물
                map_col.append(1)
            else:
                map_col.append(0)
        se.get_engine("sname").register_entity(c)
        col.append(c)
    simple_map.append(map_col)
    mat.append(col)

for i in range(height):
    for j in range(width):
        if i != 0:
            se.get_engine("sname").coupling_relation(mat[i][j], "south",
                                                     mat[i - 1][j], "north")
        if i != height - 1:
            se.get_engine("sname").coupling_relation(mat[i][j], "north",
                                                     mat[i + 1][j], "south")
        if j != 0:
            se.get_engine("sname").coupling_relation(mat[i][j], "west",
                                                     mat[i][j - 1], "east")
        if j != width - 1:
            se.get_engine("sname").coupling_relation(mat[i][j], "east",
                                                     mat[i][j + 1], "west")

#msg = SysMessage("cell", "")
#msg.insert(["R", "L", "F", "D", "R", "F"])

#시각화파트
root = Tk()
root.title("simple map")
root.resizable(False, False)

# 창 너비, 높이, 위치 설정
width, height = 540, 540
x, y = (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() -
                                                height) / 2
root.geometry("%dx%d+%d+%d" % (width, height, x, y))  #창을 중앙에 배치

canvas = Canvas(root, width=width, height=height,
                bg="white")  #게임화면을 그리는 canvas
canvas.focus_set()
canvas.pack()
canvas.create_rectangle(0, 510, 30, 540, fill="blue")
for y in range(len(simple_map[0])):
    for x in range(len(simple_map[y])):
        if simple_map[y][x] == 1:
            canvas.create_rectangle(x * 30,
                                    510 - y * 30,
                                    x * 30 + 30,
                                    510 - y * 30 + 30,
                                    fill="black")
        # elif simple_map[y][x] == 0:
        #     canvas.create_oval(x * 30,
        #                        y * 30,
        #                        x * 30 + 30,
        #                        y * 30 + 30,
        #                        fill="blue")
root.mainloop()

A = Agent()

s = str_to_instruction()
# print("명령어 한줄 입력 :")
# str = input()
str = '''
for i in range(4): s.MoveF()
s.MoveR()
A.set_ifMove('fb', 's.MoveR()')
'''
exec(str)  # 명령어를 입력받아서 파이썬 문법으로 변환

A.list_of_instruction(s)

se.get_engine("sname").insert_input_port("start")
se.get_engine("sname").coupling_relation(None, "start", mat[0][0], "west")

se.get_engine("sname").insert_external_event("start",
                                             A)  # 만들어진 명령어 리스트를 insert
se.get_engine("sname").simulate()