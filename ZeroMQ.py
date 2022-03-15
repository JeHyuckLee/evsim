from cmath import sqrt
from concurrent.futures.process import _check_system_limits
from dis import Instruction
from doctest import FAIL_FAST
from msilib.schema import SelfReg
from pickle import GLOBAL
from re import L, T
from xml.dom.minidom import Element
from matplotlib import cm
from matplotlib.pyplot import contour

from numpy import block, insert
from GameManager_test import Agent

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime
import sys
import random

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


class command_list():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.cm_list = list()

    def R(self):
        self.cm_list.append('R')

    def L(self):
        self.cm_list.append('L')

    def F(self):
        self.cm_list.append('F')

    def B(self):
        self.cm_list.append('B')

    def blk(self, cm):
        self.blk_cm = cm

    def get_command(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.cm_list


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
            aX = msg_list[0]
            aY = msg_list[1]
            print(f"[Gm] aX:{aX} aY:{aY}")
            self.Data = self.map_data(aX, aY)
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name, "agent")  #에이전트에게 갈수있는지 없는지 알려줌
        msg.insert(self.Data)
        print(f"[Gm][out]{self.Data.keys()}")
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

    def map_data(self, j, i):

        map_data = {
            'R': map[i + 1][j],
            'L': map[i - 1][j],
            'F': map[i][j + 1],
            'B': map[i][j + 1]
        }
        return map_data


class Agent(BehaviorModelExecutor, command_list):

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
            self._cur_state = "MOVE"

        elif port == "gm":  #게임매니져 에게 다음셀로 갈수있는지 여부를 받음
            print("[agent][in]")
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_list = data[0]
            self.map_data = msg_list
            self._cur_state = "OUT"

    def output(self):
        if (self._cur_state == "MOVE"):  #에이전트가 gm에게 명령어 와 자신의 현재 위치를 보냄
            Data = [self.ix, self.iy]
            msg = SysMessage(self.get_name, "gm")
            print(f"[agent][out] : {Data}")
            msg.insert(Data)
            return msg

        if (self._cur_state == "OUT"):
            while (self.cm_list == None):
                cm = self.cm_list.pop(0)
                print(f"[agent] [cm] = {cm}, [rest cmlist] = {self.cm_list}")
                if (self.map_data[cm] == 0):
                    self.move(cm)
                    print(f"[agent] move X:{self.ix},Y:{self.iy}\n")
                else:
                    print("[agent] can't go\n")
                    self.cm_list.insert(0, self.blk_cm)

    def move(self, cm):

        if (cm == "R"):
            self.ix += 1
        elif (cm == "L"):
            self.ix -= 1
        elif (cm == "F"):
            self.iy += 1
        elif (cm == "B"):
            self.iy -= 1

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

agent = Agent(0, Infinite, "agent", "sname", 1, 1)
se.get_engine("sname").register_entity(agent)

se.get_engine("sname").coupling_relation(None, "start", agent, "start")
se.get_engine("sname").coupling_relation(agent, "gm", gm, "agent")
se.get_engine("sname").coupling_relation(gm, "agent", agent, "gm")

Move = command_list()
print("ang")
for i in range(10):
    Move.F()
    Move.Blk('R')

se.get_engine("sname").insert_external_event("start", Move.get_command())
se.get_engine("sname").simulate()
