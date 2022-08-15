from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from type_def import *

class PlayerMove(BehaviorModelExecutor):
    def __init__(self, instantiate_time=..., destruct_time=..., name=".", engine_name="default"):
        BehaviorModelExecutor.__init__(instantiate_time, destruct_time, name, engine_name)

        self.pos = Position
        self.pos.set_pos(1, 1)
        self.ahead = Ahead

        self.init_state("IDLE")
        self.insert_state("IDLE",Infinite)
        self.insert_state("MOVE",1)

        self.insert_input_port("start")
        self.insert_input_port("think")
        self.insert_output_port("in")

    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "MOVE"

        elif port == "think":
            self.cancel_rescheduling()
            data = msg.retrieve()
            self.ahead = data[0]
            self.move_player(self.ahead.front)
            self._cur_state = "MOVE"

    def output(self):
        print(f"Current Position: ({self.pos.x}, {self.pos.y})")
        msg = SysMessage(self.get_name(), "in")
        msg.insert(self.pos)
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

    def move_player(self, dir):
        if dir == Direction.DIR_NORTH:
            self.pos.set_pos(self.pos.x, self.pos.y-1)
        elif dir == Direction.DIR_EAST:
            self.pos.set_pos(self.pos.x+1, self.pos.y)
        elif dir == Direction.DIR_WEST:
            self.pos.set_pos(self.pos.x-1, self.pos.y)
        elif dir == Direction.DIR_SOUTH:
            self.pos.set_pos(self.pos.x, self.pos.y+1)

class PlayerThink(BehaviorModelExecutor):
    def __init__(self, instantiate_time=..., destruct_time=..., name=".", engine_name="default"):
        BehaviorModelExecutor.__init__(instantiate_time, destruct_time, name, engine_name)

        self.pos = Position
        self.ahead = Ahead
        self.ahead.set_ahead(Direction.DIR_SOUTH)
        self.input_msg = []
        self.flag = False
        self.right_flag = False

        self.init_state("IDLE")
        self.insert_state("IDLE",Infinite)
        self.insert_state("THINK",1)

        self.insert_input_port("player")
        self.insert_output_port("move")

    def ext_trans(self, port, msg):
        if port == "player":
            self.cancel_rescheduling()
            data = msg.retrieve()
            self.input_msg.append(data[0])
            self._cur_state = "THINK"


    def output(self):
        for msg_ahead in self.input_msg:
            if self.ahead.right == msg_ahead.dir and self.right_flag == False:
                if msg_ahead.block == 0:
                    self.ahead.turn_right()
                    msg = SysMessage(self.get_name(), "move")
                    msg.insert(self.ahead)
                    self.flag = True
                    return msg
                elif msg_ahead.block == 1:
                    self.right_flag = True
            elif self.right_flag == True:
                if msg_ahead.dir == self.ahead.front:
                    if msg_ahead.block == 0:
                        msg = SysMessage(self.get_name(), "move")
                        msg.insert(self.ahead)
                        self.flag = True
                        return msg
                    elif msg_ahead.block == 1:
                        self.ahead.turn_left()
        return None

    def int_trans(self):
        if self._cur_state == "THINK" and self.flag == True:
            self._cur_state = "IDLE"
        else:
            self._cur_state = "THINK"            
