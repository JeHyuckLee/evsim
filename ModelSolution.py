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


class Cell(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name, ix, iy, is_blocked):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.set_name(f"({ix}, {iy})")
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.set_blocked(is_blocked)  
        # True = 장애물 , 장애물 인지 아닌지 set
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
        print(f"[IN]: {datetime.datetime.now()}")
        self.cancel_rescheduling()
        data = msg.retrieve()
        print(data)
        self.cm_list = data[0]
        print(self.cm_list)
        self._cur_state = "MOVE"

    def output(self):
        self.cm = self.cm_list.pop(0)

        if self.cm == "R":
            print(f"\nCurrent Location:{self.get_name()}") # 이동전 현재 위치 출력
            msg = SysMessage(self.get_name(), "east") # Right니까 east(동쪽) 이동하도록
            print(f"[OUT]: {datetime.datetime.now()}") # 현재 시간 출력

            # 만약 가려는 방향이 장애물이라면,
            if (self.get_blocked() == True): # get_blocked() 는 definition.py에 있음

                print("***The current cell is blocked.***") # 장애물 마주쳤다는 메세지 출력
                msg = SysMessage(self.get_name(), "west")  # 왔던곳으로 다시 돌아간다.

                next = input("Go back to prev-location. Input new Command : ") # 직전 위치로 돌아왔음을 알려주고, 새로운 방향 입력
                
                # 명령어 리스트의 맨 앞에 위에서 입력 받은 새로운 방향 명령 추가
                if next == "F" :
                    s.get_instruction().insert(0, next)
                elif next == "L" :
                    s.get_instruction().insert(0, next)
                elif next == "B" :
                    s.get_instruction().insert(0, next)

            msg.insert(self.cm_list)
            return msg

        elif self.cm == "F":
            print(f"\nCurrent Location:{self.get_name()}")
            
            if (self.get_blocked() == True):
                print("***The current cell is blocked.***")
                msg = SysMessage(self.get_name(), "south")

                next = input("Go back to prev-location. Input new Command : ")
                if next == "L" :
                    self.cm_list.insert(0, next)
                elif next == "R" :
                    self.cm_list.insert(0, next)
                elif next == "B" :
                    s.get_instruction().insert(0, next)

            msg = SysMessage(self.get_name(), "north")

            print(f"[OUT]: {datetime.datetime.now()}")
            
            msg.insert(self.cm_list)
            return msg

        elif self.cm == "L":
            print(f"\nCurrent Location:{self.get_name()}")
            msg = SysMessage(self.get_name(), "west")

            print(f"[OUT]: {datetime.datetime.now()}")
            #print("Next location: (1,0)")
            if (self.get_blocked() == True):
                print("***The current cell is blocked.***")
                msg = SysMessage(self.get_name(), "east")

                next = input("Go back to prev-location. Input new Command : ")
                if next == "F" :
                    s.get_instruction().insert(0, next)
                elif next == "R" :
                    s.get_instruction().insert(0, next)
                elif next == "B" :
                    s.get_instruction().insert(0, next)

            msg.insert(self.cm_list)
            return msg

        elif self.cm == "B":
            print(f"\nCurrent Location:{self.get_name()}")
            msg = SysMessage(self.get_name(), "south")
            print(f"[OUT]: {datetime.datetime.now()}")
            #print("Next location: (1,0)")
            if (self.get_blocked() == True):
                print("***The current cell is blocked.***")
                msg = SysMessage(self.get_name(), "north")

                next = input("Go back to prev-location. Input new Command : ")
                if next == "F" :
                    s.get_instruction().insert(0, next)
                elif next == "R" :
                    s.get_instruction().insert(0, next)
                elif next == "L" :
                    s.get_instruction().insert(0, next)


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
for i in range(height):
    col = list()
    for j in range(width):
        if i == 0 and j == 0:  # 시작점은 장애물 x
            c = Cell(0, Infinite, "", "sname", i, j, False)
        else:
            c = Cell(0, Infinite, "", "sname", i, j, random.choice([True, False, False, False]))  # 랜덤으로 장애물 생성  True = 장애물
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
#msg.insert(["R", "L", "F", "B", "R", "F"])


se.get_engine("sname").insert_input_port("start")
se.get_engine("sname").coupling_relation(None, "start", mat[0][0], "west")

state = ""

s = str_to_instruction()
print("명령어 입력 :")
str = input()
exec(str)  # 명령어를 입력받아서 파이썬 문법으로 변환

se.get_engine("sname").insert_external_event("start", s.get_instruction())  # 만들어진 명령어 리스트를 insert
se.get_engine("sname").simulate()
