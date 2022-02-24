from cmath import sqrt
from dis import Instruction
from doctest import FAIL_FAST
from re import T

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
        print(self.cm_list)

        self._cur_state = "MOVE"

    def output(self):

        self.cm = self.cm_list.pop(0)
        print(f"[{self.ix}, {self.iy}][OUT]: {datetime.datetime.now()}")

        if self.cm == "R":
            #쿼리, 주위의셀의 정보를 가져오도록 numpy 주위의셀을 array로

            #UI

            msg = SysMessage(self.get_name(), "east")
            if (self.get_blocked() == True):  # 만약 장애물이라면
                # get_blocked() 는 definition.py 에 있음
                msg = SysMessage(self.get_name(), "west")  # 왔던곳으로 다시 돌아간다.
                self.agent.set_flag('rb')
                print("***The current cell is blocked.***")
                self.cm_list.insert(0, self.cm)
                self.agent.ifMove()
                self.agent.set_flag(None)

        elif self.cm == "F":
            msg = SysMessage(self.get_name(), "north")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "south")
                self.agent.set_flag('fb')
                print("***The current cell is blocked.***")
                self.cm_list.insert(0, self.cm)
                self.agent.ifMove()
                self.agent.set_flag(None)

        elif self.cm == "L":
            msg = SysMessage(self.get_name(), "west")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "east")
                self.agent.set_flag('lb')
                print("***The current cell is blocked.***")
                self.cm_list.insert(0, self.cm)
                self.agent.ifMove()
                self.agent.set_flag(None)

        elif self.cm == "D":
            msg = SysMessage(self.get_name(), "south")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "north")
                self.agent.set_flag('db')
                print("***The current cell is blocked.***")
                self.cm_list.insert(0, self.cm)
                self.agent.ifMove()
                self.agent.set_flag(None)

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
        self.instructions = list()
        #변수명 깔끔하게

    def MoveR(self):
        self.instructions.append('R')

    def MoveL(self):
        self.instructions.append('L')

    def MoveF(self):
        self.instructions.append('F')

    def MoveD(self):
        self.instructions.append('B')

    def get_instruction(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.instructions


class Agent():

    def __init__(self):
        self.cm_s = ''
        self.cm_list = []
        self.flag = ''

    def set_ifMove(self, block, move):
        if block == 'rb':
            self.set_rbMove = move
        elif block == 'lb':
            self.set_lbMove = move
        elif block == 'fb':
            self.set_fbMove = move
        elif block == 'db':
            self.set_dbMove = move

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
        elif self.flag == 'db':
            if self.set_dbMove == None:
                return
            exec(self.set_dbMove)

    def list_of_instruction(self, s):
        self.cm_s = s
        for i in range(4):
            s.MoveF()

    def get_instruction(self):  # 만들어진 명령어 리스트를 반환한다.
        self.cm_list = self.cm_s.get_instruction()
        return self.cm_list

    def set_flag(self, flag):
        self.flag = flag


class agent():

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(x * 30,
                                     y * 30,
                                     x * 30 + 30,
                                     y * 30 + 30,
                                     fill="red")
        self.x, self.y = x, y
        self.nx, self.ny = x, y

    def move(self, direction):
        if direction == 'L':
            self.nx, self.ny = self.x, self.y - 1
        elif direction == 'B':
            self.nx, self.ny = self.x - 1, self.y
        elif direction == 'R':
            self.nx, self.ny = self.x, self.y + 1
        elif direction == 'F':
            self.nx, self.ny = self.x + 1, self.y
        self.canvas.move(self.id, (self.nx - self.x) * 30,
                         (self.ny - self.y) * 30)
        self.x, self.y = self.nx, self.ny


#1~160 객체 표현
#이후 객체조합``
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
            map_col.append(2)
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

se.get_engine("sname").insert_input_port("start")
se.get_engine("sname").coupling_relation(None, "start", mat[0][0], "west")
"""------------시각화파트----------------"""
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

for y in range(len(simple_map[0])):
    for x in range(len(simple_map[y])):
        if simple_map[y][x] == 1:
            canvas.create_rectangle(x * 30,
                                    y * 30,
                                    x * 30 + 30,
                                    y * 30 + 30,
                                    fill="black")
        elif simple_map[y][x] == 2:
            player = agent(canvas, x, y)
"""------------시각화파트----------------"""

A = Agent()

s = str_to_instruction()
print("명령어 입력 :")
str = input()
exec(str)  # 명령어를 입력받아서 파이썬 문법으로 변환

A.list_of_instruction(s)

se.get_engine("sname").simulate()
root.mainloop()
#에이전트도 모델, 환경도 모델로 구현
#현재위치에서 주위의 정보를 전달
#low level 에서 구현

#모델을 추가 모든 에이전트는 그 모델에 연결
#매니저가 에이전트에게 현재 셀의 정보를준다.
# 1. 손으로 찾아보세요?
# 2. IF, FOR문을 알려준다.
# 3.