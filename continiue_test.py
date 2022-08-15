from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime


class Generator(BehaviorModelExecutor):  #오토마타 구현

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")  #IDLE 상태
        self.insert_state("IDLE", Infinite)  #대기 무한정 외부에서 입력을 받아야 상태가 변함
        self.insert_state("MOVE", 1)  # MOVE상태, 1초동안 기다린후 이벤트가 없으면

        self.insert_input_port("start")  #인풋 포트
        self.insert_output_port("process")  # 아우풋 포트
   
        self.msg_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def ext_trans(self, port, msg):  #외부에서 이벤트가 들어올때 를 정의
        if port == "start":  #START라는 포트에서 데이터가 들어오면 상태를 IDLE -> MOVE로 변경
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"  #start를 받으면 1초단위로 move 라는 상태를 반복

    def output(
        self
    ):  # 메세지를 보냄, 프로세스를 지정, 프로세스포트와 연결된 에이전트는 전부 메세지를 받는다. 게임을 만드는 사람은 누가 메세지를받을지 포트를 지정
        msg = SysMessage(self.get_name(), "process")  #MOVE - 1초주기로 메세지를 보냄
        print(f"[Gen][OUT]: {datetime.datetime.now()}")
        msg.insert(self.msg_list.pop(0))  #메세지 리스트에서 하나를 뽑아서 보낸다.
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE" and not self.msg_list:  #MOVE 상태, 메세지가 비어있는경우 IDLE상태로 가라
            self._cur_state = "IDLE"  #보내야할 메세지가 없으면 IDLE
        else:  # 아니면 MOVE 상태
            self._cur_state = "MOVE"


class Processor(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)  #IDLE상태 대기 무한
        self.insert_state("PROCESS", 2)  # Process 상태, 2초 대기

        self.insert_input_port("process")

        self.msg_list = []

    def ext_trans(self, port, msg):
        if port == "process":
            print(f"[Proc][IN]: {datetime.datetime.now()}")
            self.cancel_rescheduling()  #리스케줄링을 취소
            data = msg.retrieve()
            self.msg_list.append(data[0])  #메세지를 받아서 append
            self._cur_state = "PROCESS"  #메세지 받아서 처리

    def output(self):  #지금까지 받은것을 출력
        print(f"[Proc][OUT]: {datetime.datetime.now()}")
        print("|".join(map(str, self.msg_list)))
        time = datetime.datetime.now()
        end = time - start
        print(end)
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"


# System Simulator Initialization
se = SystemSimulator()  #백엔드 생성(메안서버 )
start = datetime.datetime.now()
se.register_engine("sname", "VIRTURE_TIME",
                   1)  #로비에서 방하나만든다..? REAL_TIME => 사람의 1초 = 컴퓨터의 1초
#버츄어타임 => 시간개념 x 우선순위 부여라는 느낌,   1=> time resolution 시간을 얼마나 잘게 볼것이냐  1= 1초마다 이벤트 유뮤를 확인
se.get_engine("sname").insert_input_port(
    "start")  # input_port("start) => 포트라는 개념, API를 String 형태로 정의..?

gen = Generator(
    5, Infinite, "Gen",
    "sname")  # Generator => npc, (0= npc 가 태어나는 순간, 수명,"Gen" 이름, sname =소속된방)
se.get_engine("sname").register_entity(gen)  #register_entity 에이전트 추가

proc = Processor(6, Infinite, "Proc", "sname")  #
se.get_engine("sname").register_entity(proc)  #에이전트 추가

se.get_engine("sname").coupling_relation(
    None, "start", gen, "start")  #방(start라는 포트와 )과 gen 의 start 연결
se.get_engine("sname").coupling_relation(gen, "process", proc,
                                         "process")  #에이전트 간의 상호작용..? 입출력 연결

se.get_engine("sname").insert_external_event("start", None)  #외부에서 이벤트를 꽂아줌
se.get_engine("sname").simulate()  #게임시작
