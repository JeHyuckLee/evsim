from cmath import sqrt
from concurrent.futures.process import _check_system_limits
from dis import Instruction
from doctest import FAIL_FAST
from msilib.schema import SelfReg

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from Agent import *
from Game_manager import *

#게임활용의 수업, 운영


class command_list():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.cm_list = list()

        self.rblk_cm = ''
        self.lblk_cm = ''
        self.fblk_cm = ''
        self.bblk_cm = ''

    def R(self):
        self.cm_list.append('R')

    def L(self):
        self.cm_list.append('L')

    def F(self):
        self.cm_list.append('F')

    def B(self):
        self.cm_list.append('B')

    def Blk(self, blk, cm):
        if blk == 'R':
            self.rblk_cm = cm
        elif blk == 'L':
            self.lblk_cm = cm
        elif blk == 'F':
            self.fblk_cm = cm
        elif blk == 'B':
            self.bblk_cm = cm

    def get_blk(self, blk):
        if blk == 'R':
            return self.rblk_cm
        elif blk == 'L':
            return self.lblk_cm
        elif blk == 'F':
            return self.fblk_cm
        elif blk == 'B':
            return self.bblk_cm

    def get_command(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.cm_list


# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("command")

gm = Gamemanager(0, Infinite, "gm", "sname")
se.get_engine("sname").register_entity(gm)

agent = Agent(0, Infinite, "agent", "sname", 1, 1)  #에이전트의 시작위치 지정
se.get_engine("sname").register_entity(agent)

se.get_engine("sname").coupling_relation(None, "command", agent, "command")

se.get_engine("sname").coupling_relation(agent, "gm", gm, "agent")
se.get_engine("sname").coupling_relation(gm, "agent", agent, "gm")

Move = command_list()

# 명령어 파트 시작

Move.Blk('F', 'R')
for i in range(10):
    Move.F()

# 끝

if Move.get_blk('R') != None:
    agent.Set_Ifmove('R', Move.get_blk('R'))
if Move.get_blk('L') != None:
    agent.Set_Ifmove('L', Move.get_blk('L'))
if Move.get_blk('F') != None:
    agent.Set_Ifmove('F', Move.get_blk('F'))
if Move.get_blk('B') != None:
    agent.Set_Ifmove('B', Move.get_blk('B'))

se.get_engine("sname").insert_external_event("command", Move.get_command())
se.get_engine("sname").simulate()
