from tracemalloc import start
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
        self.msg_list = []
        self.insert_input_port("start")  #인풋 포트
        self.insert_output_port("process")  # 아우풋 포트

        for i in range(1):
            self.msg_list.append(i)

    def ext_trans(self, port, msg):  #외부에서 이벤트가 들어올때 를 정의
        if port == "start":  #START라는 포트에서 데이터가 들어오면 상태를 IDLE -> MOVE로 변경
            self._cur_state = "MOVE"  #start를 받으면 1초단위로 move 라는 상태를 반복

    def output(
        self
    ):  # 메세지를 보냄, 프로세스를 지정, 프로세스포트와 연결된 에이전트는 전부 메세지를 받는다. 게임을 만드는 사람은 누가 메세지를받을지 포트를 지정
        msg = SysMessage(self.get_name(), "process")  #MOVE - 1초주기로 메세지를 보냄
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
            self.cancel_rescheduling()  #리스케줄링을 취소
            data = msg.retrieve()
            self.msg_list.append(data[0])  #메세지를 받아서 append
            self._cur_state = "PROCESS"  #메세지 받아서 처리

    def output(self):  #지금까지 받은것을 출력
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"


Start_time = datetime.datetime.now()
print(f"Start : {Start_time}")
# System Simulator Initialization
se = SystemSimulator()  #백엔드 생성(메안서버 )
se.register_engine("sname", "VIRTURE_TIME", 1)
se.get_engine("sname").insert_input_port("start")
for i in range(1):
    gen_name = "gen" + str(i)
    pro_name = "pro" + str(i)
    gen_name = Generator(0, Infinite, "Gen", "sname")
    se.get_engine("sname").register_entity(gen_name)
    pro_name = Processor(0, Infinite, "Proc", "sname")
    se.get_engine("sname").register_entity(pro_name)
    se.get_engine("sname").coupling_relation(None, "start", gen_name, "start")
    se.get_engine("sname").coupling_relation(gen_name, "process", pro_name,
                                             "process")
se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()
time = datetime.datetime.now()
end = time - Start_time
print(f"Running_time :{end.seconds}s {end.microseconds}ms")
