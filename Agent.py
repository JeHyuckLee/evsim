from concurrent.futures import thread
from ctypes.wintypes import tagRECT
from trace import Trace
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
        self.insert_state("SEND", 0.01)
        self.insert_state("MOVE", 0.01)
        self.insert_state("END", Infinite)
        self.insert_input_port("agent")
        self.insert_output_port("gm")
        self.insert_input_port("command")
        self.insert_input_port("blk")
        self.insert_input_port("test")
        self.ix = ix
        self.iy = iy
        self.blk_flag = False
        self.flag = ''

    def ext_trans(self, port, msg):
        msg_list = []
        print(f"exttrans {self.get_cur_state()}")

        if port == "command":  #명령어 리스트를 입력받음
            print("[agent][start]")
            self.cancel_rescheduling()
            data = msg.retrieve()
            self.cm_list = data[0]
            print(f"[agent][in] cm_list :{self.cm_list} ")
            self._cur_state = "SEND"  #SEND state = GM에게 자신의 현재위치를 보냄

        elif port == "gm":  #게임매니져 에게 현재위치에 대한 주변 정보를 얻음
            print("[agent][in]")
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_list = data[0]
            self.map_data = msg_list
            self._cur_state = "MOVE"  #MOVE state = 움직일수있는지 여부를 판단해서 움직임

    def output(self):
        print(f"output {self.get_cur_state()}")

        if self._cur_state == "SEND":  #에이전트가 gm에게 자신의 현재 위치를 보냄
            Data = [self.ix, self.iy]
            msg = SysMessage(self.get_name, "gm")
            print(f"[agent][current] : {Data}")
            msg.insert(Data)
            return msg

        if self._cur_state == "MOVE":  #에이전트가 움직인다.
            cm = self.cm_list.pop(0)
            try:
                print(f"[agent] [cm] = {cm}, [rest cmlist] = {self.cm_list}")
                if (self.map_data[cm] == 0):  #장애물이 없는경우
                    self.move(cm)
                    print(f"[agent] move X:{self.ix},Y:{self.iy}\n")

                elif (self.map_data[cm] == 1):  #장애물을 만난경우
                    print(f"[agent] can't go")
                    self.flag = cm
                    print(f"[agent] if move")
                    self.Ifmove()  #설정해둔 if move
                    self.blk_flag = True

                elif (self.map_data[cm] == 3):  #도착지점에 도착
                    self.move(cm)
                    print(f"[agent] move X:{self.ix},Y:{self.iy}\n")
                    print("[agent] arrive!")
                    self._cur_state = "END"  #게임엔드
            except:
                self._cur_state = "END"  #모든부분에서 막혀있을경우 게임을 종료한다.

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
            self.cm_list.insert(0, self.rblk_move)
        elif self.flag == 'L':
            self.cm_list.insert(0, self.lblk_move)
        elif self.flag == 'F':
            self.cm_list.insert(0, self.fblk_move)
        elif self.flag == 'B':
            self.cm_list.insert(0, self.bblk_move)

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
        print(f"int trans {self.get_cur_state()}")

        if self._cur_state == "END":  #게임엔드
            print("GAME END")

        elif self.blk_flag == True:  #벽을만났을때 리스트에 ifmove에서 설정한 방향을 추가하고, 다시 Move로 이동
            self._cur_state == "MOVE"
            self.blk_flag = False

        elif self._cur_state == "SEND":  #GM에게 메세지를 보낸후 다시 IDLE 상태로 GM에게 메시지 받을때 까지 대기
            self._cur_state = "IDLE"

        elif not self.cm_list:
            self._cur_state == "END"

        else:  #MOVE 한 이후 SEND상태로 가서 다시 GM에게 현재위치 를 전송
            self._cur_state = "SEND"
