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
        print("\n")
        print(f"[{self.ix}, {self.iy}][IN]: {datetime.datetime.now()}")
        self.cancel_rescheduling()
        data = msg.retrieve()
        # print(data)
        self.cm_list = data[0]
        print(f"Current Location:{self.get_name()}")
        print("instruction list : ", self.cm_list)
        self._cur_state = "MOVE"

    def output(self):
        self.cm = self.cm_list.pop(0)
        print(f"[{self.ix}, {self.iy}][OUT]: {datetime.datetime.now()}")

        all_cm = ["R", "F", "L", "B"]

        if self.cm == "R":
            msg = SysMessage(self.get_name(), "east")
            if (self.get_blocked() == True):  # 만약 장애물이라면
                # get_blocked() 는 definition.py 에 있음
                msg = SysMessage(self.get_name(), "west")  # 왔던곳으로 다시 돌아간다.
                print(f"***The current cell[{self.get_name()}] is blocked.***")
                self.cm_list.insert(0, self.cm)

                next = input("Go back to prev-location. Input new Command : "
                             )  # 이전 위치로 돌아왔음을 알려주고, 새로운 방향 입력

                # 명령어 리스트의 맨 앞에 위에서 입력 받은 새로운 방향 명령 추가
                next = input("Go back to prev-location. Input new Command : ")
                if next in all_cm :
                    self.cm_list.insert(0, next)
                else :
                    print(f"***The command[{next}] is impossible.***")

        elif self.cm == "F":
            msg = SysMessage(self.get_name(), "north")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "south")
                print(f"***The current cell[{self.get_name()}] is blocked.***")
                self.cm_list.insert(0, self.cm)

                next = input("Go back to prev-location. Input new Command : ")
                if next in all_cm :
                    self.cm_list.insert(0, next)
                else :
                    print(f"***The command[{next}] is impossible.***")

        elif self.cm == "L":
            msg = SysMessage(self.get_name(), "west")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "east")
                print(
                    f"***The current cell [{self.get_name()}] is blocked.***")
                self.cm_list.insert(0, self.cm)

                next = input("Go back to prev-location. Input new Command : ")
                if next in all_cm :
                    self.cm_list.insert(0, next)
                else :
                    print(f"***The command[{next}] is impossible.***")

        elif self.cm == "B":
            msg = SysMessage(self.get_name(), "south")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "north")
                print(f"***The current cell[{self.get_name()}] is blocked.***")
                self.cm_list.insert(0, self.cm)

                next = input("Go back to prev-location. Input new Command : ")
                if next in all_cm :
                    self.cm_list.insert(0, next)
                else :
                    print(f"***The command[{next}] is impossible.***")

        msg.insert(self.cm_list)
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"


class str_to_instruction():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.list_of_instruction = list()

    def MoveR(self):
        self.list_of_instruction.append('R')

    def MoveL(self):
        self.list_of_instruction.append('L')

    def MoveF(self):
        self.list_of_instruction.append('F')

    def MoveB(self):
        self.list_of_instruction.append('B')

    def get_instruction(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.list_of_instruction


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

for y in range(len(simple_map[0])):
    for x in range(len(simple_map[y])):
        if simple_map[y][x] == 1:
            canvas.create_rectangle(x * 30,
                                    y * 30,
                                    x * 30 + 30,
                                    y * 30 + 30,
                                    fill="black")
        # elif simple_map[y][x] == 0:
        #     canvas.create_oval(x * 30,
        #                        y * 30,
        #                        x * 30 + 30,
        #                        y * 30 + 30,
        #                        fill="blue")
root.mainloop()

s = str_to_instruction()
print("명령어 입력 :")
str = input()
exec(str)  # 명령어를 입력받아서 파이썬 문법으로 변환

se.get_engine("sname").insert_external_event("start", s.get_instruction())  # 만들어진 명령어 리스트를 insert

se.get_engine("sname").simulate()
