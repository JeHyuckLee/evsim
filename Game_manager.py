from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from system_simulator import SystemSimulator

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
        print(f"[Gm][out]{self.Data}")
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