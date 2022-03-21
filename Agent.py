from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from system_simulator import SystemSimulator


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
        self.insert_input_port("command")
        self.insert_input_port("blk")

        self.ix = ix
        self.iy = iy

        self.flag = ''

    def ext_trans(self, port, msg):
        msg_list = []
        if port == "command":  #명령어 리스트를 입력받음
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
            print(f"[agent][current] : {Data}")
            msg.insert(Data)
            return msg

        if (self._cur_state == "OUT"):
            cm = self.cm_list.pop(0)
            print(f"[agent] [cm] = {cm}, [rest cmlist] = {self.cm_list}")
            if (self.map_data[cm] == 0):
                self.move(cm)
                print(f"[agent] move X:{self.ix},Y:{self.iy}\n")
            elif (self.map_data[cm] == 1):
                print(f"[agent] can't go")
                self.flag = cm
                print(f"[agent] ifmove")
                self.Ifmove()
            elif (self.map_data[cm] == 3):
                self.move(cm)
                print(f"[agent] move X:{self.ix},Y:{self.iy}\n")
                print("[agent] arrive!")

    def Set_Ifmove(self, blk, cm):
        if blk == 'R':
            self.rblk_move = cm
        elif blk == 'L':
            self.lblk_move = cm
        elif blk == 'F':
            self.fblk_move = cm
        elif blk == 'B':
            self.bblk_move = cm

    def Ifmove(self):
        if self.flag == 'R':
            self.move(self.rblk_move)
        elif self.flag == 'L':
            self.move(self.lblk_move)
        elif self.flag == 'F':
            self.move(self.fblk_move)
        elif self.flag == 'B':
            self.move(self.bblk_move)

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