from re import T
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from system_simulator import SystemSimulator
from Agent import *
from Game_manager import *
from tkinter import *
from tkinter import messagebox

# IDLE 상태에서 대기하다가 ext_trans 에서 이벤트를 받음  이벤트를 받은후 cur_state를 변경하고 output으로 이동 output 에서 처리가 끝나면 int_trans 를 통해 다시 cur_state를 조절
# cur_state가 다시 IDLE이 되면 이벤트를 받을때 까지 대기 , 다른 state로 바뀌면 다시 output으로 이동 해서 처리


class command_list():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.cm_list = list()

        self.rblk_cm = None
        self.lblk_cm = None
        self.fblk_cm = None
        self.bblk_cm = None

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

se.register_engine("sname", "REAL_TIME", 0.01)
se.get_engine("sname").insert_input_port("nonblock")

se.register_engine("sname2", "REAL_TIME", 0.01)

se.get_engine("sname2").insert_input_port("command")
se.get_engine("sname2").insert_input_port("test")

gm = Gamemanager(0, Infinite, "gm", "sname")
se.get_engine("sname2").register_entity(gm)

agent = Agent(0, Infinite, "agent", "sname", 1, 1)  #에이전트의 시작위치 지정
se.get_engine("sname2").register_entity(agent)

se.get_engine("sname2").coupling_relation(None, "command", agent, "command")

se.get_engine("sname2").coupling_relation(None, "test", agent, "test")

se.get_engine("sname2").coupling_relation(agent, "gm", gm, "agent")
se.get_engine("sname2").coupling_relation(gm, "agent", agent, "gm")

Move = command_list()

# 명령어 파트 시작

Move.Blk('F', 'R')
Move.Blk('R', 'L')
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

#se.get_engine("sname").simulate()
print("DD")
se.exec_non_block_simulate(["sname", "sname2"])
se.get_engine("sname2").insert_external_event("command", Move.get_command())