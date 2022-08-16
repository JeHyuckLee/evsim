from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from maze_cell import *
from player import *
from type_def import *
import datetime

se = SystemSimulator()

start = datetime.datetime.now()

se.register_engine("sname", "VIRTURE_TIME", 1)
se.get_engine("sname").insert_input_port("start")

move = PlayerMove(0, Infinite, "move", "sname", 1, 1)
think = PlayerThink(0, Infinite, "think", "sname")
se.get_engine("sname").register_entity(move)
se.get_engine("sname").register_entity(think)
se.get_engine("sname").coupling_relation(None, "start", move, "start")
se.get_engine("sname").coupling_relation(think, "move", move, "think")

cell_in = CellIn(0, Infinite, "cell", "sname")
cell_check = CellCheck(0, Infinite, "check", "sname")
se.get_engine("sname").register_entity(cell_in)
se.get_engine("sname").register_entity(cell_check)
se.get_engine("sname").coupling_relation(cell_in, "check", cell_check, "check")

se.get_engine("sname").coupling_relation(move, "in", cell_in, "in")
se.get_engine("sname").coupling_relation(cell_check, "player", think, "player")

se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()