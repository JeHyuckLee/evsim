from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from type_def import *

maze_cell = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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


class CellIn(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)
        self.insert_state("IN", 0)
        self.insert_state("IDLE", Infinite)
        self.init_state("IDLE")

        self.insert_output_port("check")
        self.insert_input_port("in")

        self.pos = Position(0, 0)

    def ext_trans(self, port, msg):
        if port == "in":
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_pos = data[0]
            self.pos.set_pos(msg_pos.get_pos())

    def output(self):
        msg = SysMessage(self.get_name, "check")
        msg.insert(self.pos)

        return msg

    def int_trans(self):
        if self._cur_state == "IN":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"


class CellCheck(BehaviorModelExecutor):
    cell_msg = []

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)
        self.insert_state("CHECK", 0)
        self.insert_state("IDLE", Infinite)
        self.init_state("IDLE")
        self.pos = Position(0, 0)
        self.insert_input_port("check")
        self.insert_output_port("out")

    def ext_trans(self, port, msg):
        if port == "check":
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_pos = data[0]
            self.pos.set_pos(msg_pos.get_pos())

    def output(self):
        x, y = self.pos.get_pos()
        north = cell_msg(direction=Direction.Dir_Nort,
                         x=x,
                         y=y + 1,
                         block=maze_cell[x][y + 1])
        east = cell_msg(direction=Direction.Dir_East,
                        x=x + 1,
                        y=y,
                        block=maze_cell[x + 1][y])
        west = cell_msg(direction=Direction.Dir_East,
                        x=x - 1,
                        y=y,
                        block=maze_cell[x - 1][y])
        south = cell_msg(direction=Direction.Dir_East,
                         x=x,
                         y=y - 1,
                         block=maze_cell[x][y - 1])

        cell_msg = [north, east, west, south]

        msg = SysMessage(self.get_name, "out")
        msg.insert(cell_msg)

        return msg

    def int_trans(self):
        if self._cur_state == "CHECK":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"

class Cell:
    def __init__(self, instantiate_time=..., destruct_time=..., name=".", engine_name="default"):
        self.cell_in = CellIn(instantiate_time, destruct_time, name, engine_name)
        self.cell_check = CellCheck(instantiate_time, destruct_time, name, engine_name)