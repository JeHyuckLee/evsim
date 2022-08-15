from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from player import *
from type_def import *
import datetime

se = SystemSimulator()

start = datetime.datetime.now()

se.register_engine("sname", "VIRTURE_TIME", 1)
se.get_engine("sname").insert_input_port("start")

gen = PlayerMove(0, Infinite, "Player", "sname")
se.get_engine("sname").register_entity(gen)

proc = Processor(0, Infinite, "Proc", "sname") #
se.get_engine("sname").register_entity(proc) #에이전트 추가

se.get_engine("sname").coupling_relation(None, "start", gen, "start") #방(start라는 포트와 )과 gen 의 start 연결
se.get_engine("sname").coupling_relation(gen, "process", proc, "process") #에이전트 간의 상호작용..? 입출력 연결

se.get_engine("sname").insert_external_event("start", None) #외부에서 이벤트를 꽂아줌  
se.get_engine("sname").simulate() #게임시작