from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 시뮬레이션 엔진이 주기적으로 챗봇에 데이터를 보내주면 시뮬레이션에서 현실과의 연결이 됨 => 능동적으로 메시지를 보내주는 api를 찾아야함
class Generator(BehaviorModelExecutor): #오토마타 구현
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE") #초기 상태
        self.insert_state("IDLE", Infinite) #idle 상태 (대기상태), 무한대로 대기하도록 => 외부에서 입력이 올 떄까지 무한대로 대기
        self.insert_state("MOVE", 1) #move 상태인데 대기시간이 1, 1초동안 이벤트 없으면 인터널 트랜지셔널 일어남

        self.insert_input_port("start") 
        self.insert_output_port("process") #바깥으로 나가는거
        self.msg_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #컨텐츠 만들어놓음

    def ext_trans(self,port, msg): #외부에서 이벤트가 들어왔을 때의 동작
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name(), "process") #보내는 사람 이름과 process로 지정해서 여기와 연결되어 있는 것들은 전부 메시지를 받음
        print(f"[Gen][OUT]: {datetime.datetime.now()}") 
        msg.insert(self.msg_list.pop(0))
        return msg
        
    def int_trans(self):
        if self._cur_state == "MOVE" and not self.msg_list: #보내야될 메시지가 하나도 없으면 idle로 그렇지 않으면 move에 남아있어라 => move에서 1초단위로 메시지 보내기 시작함
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

class Processor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 2) #2초동안 기다림

        self.insert_input_port("process")

        self.updater = Updater("5070853505:AAEwqzotE-qYbsLwtngMlepqs2GzaseQiBI")
        self.updater.bot.send_message(5022425918, "sim_start")

        self.msg_list = []

    def ext_trans(self,port, msg):
        if port == "process":
            print(f"[Proc][IN]: {datetime.datetime.now()}")
            self.cancel_rescheduling() # 메시지를 보냈을때 스케줄이 전부 취소되는데 그걸 막음
            data = msg.retrieve()
            self.msg_list.append(data[0]) #데이터 집어넣음
            self._cur_state = "PROCESS"

    def output(self):
        print(f"[Proc][OUT]: {datetime.datetime.now()}")
        print("|".join(map(str, self.msg_list)))
        self.updater.bot.send_message(5022425918, "|".join(map(str, self.msg_list)))
        return None
        

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"

#이 밑은 전부 관리자 모드
# System Simulator Initialization
se = SystemSimulator() #백엔드 서버 만들려고 가져옴 (카드라이더 메인 서버)

se.register_engine("sname", "REAL_TIME", 1) #로비에서 방 하나 만들기 등을 위해 만들음 (멀티 구현은 확실치 않음)
#real time : 사람의 1초와 컴퓨터의 1초를 같게 함
#1 : time resolution = 시간을 얼마나 잘게 볼 것인지 => 1초 단위로 이벤트가 있는지 없는지 확인 (너무 자주하면 성능 떨어짐)
se.get_engine("sname").insert_input_port("start") # sname 로비 가져옴, insert_input_port : 사용자가 입력을 주면 해당되는 로비에게 명령을 줌

gen = Generator(0, Infinite, "Gen", "sname") #generator:npc, 0:npc가 태어나는 순간 지정, infinite:수명 무한대, gen:npc 이름, sname:npc가 소속된 방
se.get_engine("sname").register_entity(gen) # register_entity:에이전트 추가

proc = Processor(0, Infinite, "Proc", "sname")
se.get_engine("sname").register_entity(proc) #에이전트 추가

se.get_engine("sname").coupling_relation(None, "start", gen, "start") #coupling_relation:커플 연결짓기, none:입력을 받아 처리할 수 있는 포트를 만들었는데 방과 gen을 연결시킴, start:로비의 start가 gen의 start 연결되는 것
se.get_engine("sname").coupling_relation(gen, "process", proc, "process") # gen의 프로세스와 proc의 프로세스와 연결 (출력과 입력 연결)

se.get_engine("sname").insert_external_event("start", None) # 외부에서 start 이벤트를 꽂아줌
se.get_engine("sname").simulate() #게임 시작
