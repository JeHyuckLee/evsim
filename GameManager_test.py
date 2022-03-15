from cmath import sqrt
from concurrent.futures.process import _check_system_limits
from dis import Instruction
from doctest import FAIL_FAST
from msilib.schema import SelfReg
from re import T
from xml.dom.minidom import Element
from matplotlib import cm
from matplotlib.pyplot import contour

from numpy import block, insert

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime
import sys
import random
from tkinter import *
from tkinter import messagebox

map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
       [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
       [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
       [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
       [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
       [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
       [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
       [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
       [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
       [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
       [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
       [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1],
       [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 3, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#게임활용의 수업, 운영


class Gamemanager(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.set_name(engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("agent")

        self.insert_output_port("gm")

    def ext_trans(self, port, msg):
        msg_list = []
        if port == "agent":  #에이전트에게 명령어 와 현재 위치를 받는다.
            print(f"[Gm][in] instruction received")
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_list = data[0]
            self.cm = msg_list[0]
            aX = msg_list[1]
            aY = msg_list[2]
            print(f"[Gm] cm:{self.cm} aX:{aX} aY:{aY}")
            self.bool = self.is_colide(self.cm, aX,
                                       aY)  #현재위치에서 가고자하는 셀을 갈수 있는지 여부를 판단.
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name, "agent")  #에이전트에게 갈수있는지 없는지 알려줌
        returndata = [self.bool, self.cm]
        msg.insert(returndata)
        print(f"[Gm][out]{self.bool} ,{self.cm}")
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

    def is_colide(self, cm, j, i):
        if cm == "R":
            if map[i][j + 1] == 1:
                return True
            else:
                return False
        elif cm == "L":
            if map[i][j - 1] == 1:
                return True
            else:
                return False
        elif cm == "F":
            if map[i + 1][j] == 1:
                return True
            else:
                return False
        elif cm == "B":
            if map[i - 1][j] == 1:
                return True
            else:
                return False
        else:
            print("Wrong command.")
            pass


class visualize():

    def __init__(self, x, y):
        self.ix = x
        self.iy = y
        map[self.ix][self.iy] = 2

    def visualize(self):
        root = Tk()
        root.title("미로 찾기 게임")
        root.resizable(False, False)
        # 창 너비, 높이, 위치 설정
        width, height = 540, 540
        x, y = (root.winfo_screenwidth() -
                width) / 2, (root.winfo_screenheight() - height) / 2
        root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        # canvas를 추가하고 키이벤트를 부착
        self.canvas = Canvas(root, width=width, height=height, bg="white")
        self.canvas.focus_set()
        self.canvas.pack()

        for y in range(len(map[0])):
            for x in range(len(map[y])):
                if map[y][x] == 1:
                    self.canvas.create_rectangle(x * 30,
                                                 y * 30,
                                                 x * 30 + 30,
                                                 y * 30 + 30,
                                                 fill="black")
                elif map[y][x] == 2:
                    self.id = self.canvas.create_oval(x * 30,
                                                      y * 30,
                                                      x * 30 + 30,
                                                      y * 30 + 30,
                                                      fill="red")
                elif map[y][x] == 3:
                    self.canvas.create_oval(x * 30,
                                            y * 30,
                                            x * 30 + 30,
                                            y * 30 + 30,
                                            fill="blue")
        root.mainloop()

    def move(self, x, y):
        self.nx = x
        self.ny = y
        self.canvas.move(self.id, (self.nx - self.ix) * 30,
                         (self.ny - self.iy) * 30)
        self.ix, self.iy = self.nx, self.ny


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


class Agent(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name, ix,
                 iy):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)
        self.insert_state("OUT", 1)
        self.insert_input_port("agent")
        self.insert_output_port("gm")
        self.insert_input_port("start")

        self.ix = ix
        self.iy = iy

    def ext_trans(self, port, msg):
        msg_list = []
        if port == "start":  #명령어 리스트를 입력받음
            print("[agent][start]")
            self.cancel_rescheduling()
            data = msg.retrieve()
            self.cm_list = data[0]
            print(f"[agent][in] cm_list :{self.cm_list} ")
            #시각화
            # self.v = visualize(self.ix, self.iy)
            # self.v.visualize()
            self._cur_state = "MOVE"

        elif port == "gm":  #게임매니져 에게 다음셀로 갈수있는지 여부를 받음
            print("[agent][in]")
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_list = data[0]
            self.bool = msg_list[0]
            self.cm = msg_list[1]
            self._cur_state = "OUT"

    def output(self):
        if (self._cur_state == "MOVE"):  #에이전트가 gm에게 명령어 와 자신의 현재 위치를 보냄
            cm = self.cm_list.pop(0)
            Data = [cm, self.ix, self.iy]
            msg = SysMessage(self.get_name, "gm")
            print(f"[agent][out] : {Data}")
            msg.insert(Data)
            return msg
        if (self._cur_state == "OUT"):
            if self.bool == False:
                self.move(self.cm)
                print(f"[agent] move X: {self.ix} Y: {self.iy}\n")
            else:
                print("[agent] can't go\n")

    def move(self, cm):
        if (cm == "R"):
            self.ix += 1
            self.move(self.ix, self.iy)
        elif (cm == "L"):
            self.ix -= 1
            self.move(self.ix, self.iy)
        elif (cm == "F"):
            self.iy += 1
            self.move(self.ix, self.iy)
        elif (cm == "B"):
            self.iy -= 1
            self.move(self.ix, self.iy)

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"


# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("start")

gm = Gamemanager(0, Infinite, "gm", "sname")
se.get_engine("sname").register_entity(gm)

agent = Agent(0, Infinite, "agent", "sname", 2, 2)
se.get_engine("sname").register_entity(agent)

se.get_engine("sname").coupling_relation(None, "start", agent, "start")
se.get_engine("sname").coupling_relation(agent, "gm", gm, "agent")
se.get_engine("sname").coupling_relation(gm, "agent", agent, "gm")

s = str_to_instruction()

for i in range(10):
    s.MoveF()

se.get_engine("sname").insert_external_event("start", s.get_instruction())
se.get_engine("sname").simulate()
