from cmath import sqrt
from dis import Instruction
from doctest import FAIL_FAST
from re import T
from shutil import move

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime
import sys
import random


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

        elif self.cm == "B":
            msg = SysMessage(self.get_name(), "south")
            if (self.get_blocked() == True):
                msg = SysMessage(self.get_name(), "north")
                self.agent.set_flag('bb') 
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
        self.cm_s = None # 클래스 str_to_instruction

        self.set_rbMove = None # 막혔을때 이동설정
        self.set_lbMove = None
        self.set_fbMove = None
        self.set_bbMove = None

        self.cm_list = [] # 움직임 리스트

        self.flag = None # 막힘여부 플래그
    
    def set_ifMove(self, block, MoveSet):
        if block == 'rb':
            self.set_rbMove = MoveSet
        elif block == 'lb':
            self.set_lbMove = MoveSet
        elif block == 'fb':
            self.set_fbMove = MoveSet
        elif block == 'bb':
            self.set_bbMove = MoveSet

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
                return
            exec(self.set_bbMove)
        
    def list_of_instruction(self, s):
        self.cm_s = s
        # for i in range(4): s.MoveF()

    def get_instruction(self):  # 만들어진 명령어 리스트를 반환한다.
        self.cm_list = self.cm_s.get_instruction()
        return self.cm_list
    
    def set_flag(self, flag):
        self.flag = flag

# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("start")

width = 100
height = 100

mat = list()
for i in range(height):
    col = list()
    for j in range(width):
        if i == 0 and j == 0:  # 시작점은 장애물 x
            c = Cell(0, Infinite, "", "sname", j, i, False)
        elif i == 1 and j == 0:
            c = Cell(0, Infinite, "", "sname", j, i, True)
        elif i == 0 and j == 1:
            c = Cell(0, Infinite, "", "sname", j, i, True)
        else:
            c = Cell(0, Infinite, "", "sname", j, i,
                     random.choice([True, False, False, False]))  # 랜덤으로 장애물 생성  True = 장애물
        se.get_engine("sname").register_entity(c)
        col.append(c)
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

A = Agent()

s = str_to_instruction()
# print("명령어 한줄 입력 :")
# str = input()
str = '''
for i in range(4): s.MoveF()
A.set_ifMove('fb', 's.MoveR()')
'''
exec(str)  # 명령어를 입력받아서 파이썬 문법으로 변환

print(f"명령어 : {str}")
A.list_of_instruction(s)

se.get_engine("sname").insert_input_port("start")
se.get_engine("sname").coupling_relation(None, "start", mat[0][0], "west")

se.get_engine("sname").insert_external_event("start", A)  # 만들어진 명령어 리스트를 insert
se.get_engine("sname").simulate()