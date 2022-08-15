import imp
from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from cell import *
from player import *
from type_def import *
import datetime

se = SystemSimulator()

start = datetime.datetime.now()

se.register_engine("sname", "VIRTURE_TIME", 1)
se.get_engine("sname").insert_input_port("start")

player = Player(0, Infinite, "Player", "sname")
se.get_engine("sname").register_entity(player.move)
se.get_engine("sname").register_entity(player.think)
se.get_engine("sname").coupling_relation(None, "start", player.move, "start")
se.get_engine("sname").coupling_relation(player.think, "move", player.move, "think")

cell = Cell(0, Infinite, "Cell", "sname")
se.get_engine("sname").register_entity(cell.cell_in)
se.get_engine("sname").register_entity(cell.cell_check)
se.get_engine("sname").coupling_relation(cell.cell_in, "check", cell.cell_check, "check")

se.get_engine("sname").coupling_relation(player.move, "in", cell.cell_in, "in")
se.get_engine("sname").coupling_relation(cell.cell_check, "player", player.think, "player")

se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()