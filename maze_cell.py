from dataclasses import dataclass
from turtle import pos
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from system_simulator import SystemSimulator

from type_def import *


class CellIn(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)
        self.insert_state("IN", 1)
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
            x, y = msg_pos.get_pos()
            self.pos.set_pos(x, y)
            self._cur_state = "IN"

    def output(self):
        print("output")
        msg = SysMessage(self.get_name, "check")
        msg.insert(self.pos)

        return msg

    def int_trans(self):
        if self._cur_state == "IN":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"


class CellCheck(BehaviorModelExecutor):
    cell_msg_list = []

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)
        self.insert_state("CHECK", 1)
        self.insert_state("IDLE", Infinite)
        self.init_state("IDLE")
        self.pos = Position(0, 0)
        self.insert_input_port("check")
        self.insert_output_port("player")

    def ext_trans(self, port, msg):
        if port == "check":
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_pos = data[0]
            x, y = msg_pos.get_pos()
            self.pos.set_pos(x, y)
            self._cur_state = "CHECK"

    def output(self):
        x, y = self.pos.get_pos()
        north = cell_msg(direction=Direction.DIR_NORTH,
                         x=x,
                         y=y + 1,
                         block=maze_cell[x][y + 1])
        east = cell_msg(direction=Direction.DIR_EAST,
                        x=x + 1,
                        y=y,
                        block=maze_cell[x + 1][y])
        west = cell_msg(direction=Direction.DIR_WEST,
                        x=x - 1,
                        y=y,
                        block=maze_cell[x - 1][y])
        south = cell_msg(direction=Direction.DIR_SOUTH,
                         x=x,
                         y=y - 1,
                         block=maze_cell[x][y - 1])

        self.cell_msg_list = [north, east, west, south]

        msg = SysMessage(self.get_name, "player")
        msg.insert(cell_msg)

        return msg

    def int_trans(self):
        if self._cur_state == "CHECK":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"
