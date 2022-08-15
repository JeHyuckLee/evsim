from turtle import st
from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime
import os


class Generator(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)
        self.msg_list = []
        self.insert_input_port("start")
        self.insert_output_port("process")
        for i in range(100):
            self.msg_list.append(i)

    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name(), "process")

        msg.insert(self.msg_list.pop(0))
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE" and not self.msg_list:
            self._cur_state = "IDLE"
        else:
            self._cur_state == "IDLE"


class Processor(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 1)

        self.insert_input_port("process")
        self.insert_output_port("generator")
        self.msg_list = []

    def ext_trans(self, port, msg):
        if port == "process":

            self.cancel_rescheduling()
            data = msg.retrieve()
            self.msg_list.append(data[0])
            self._cur_state = "PROCESS"

    def output(self):
        msg = SysMessage(self.get_name(), "start")
        msg.insert("ack")
        return msg

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"


Start_time = datetime.datetime.now()
print(f"Start : {Start_time}\n")
# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "VIRTUAL_TIME", 1)

se.get_engine("sname").insert_input_port("start")
for i in range(100):
    gen_name = "gen" + str(i)
    pro_name = "pro" + str(i)
    gen_name = Generator(0, Infinite, "Gen", "sname")
    se.get_engine("sname").register_entity(gen_name)
    pro_name = Processor(0, Infinite, "Proc", "sname")
    se.get_engine("sname").register_entity(pro_name)
    se.get_engine("sname").coupling_relation(None, "start", gen_name, "start")
    se.get_engine("sname").coupling_relation(gen_name, "process", pro_name,
                                             "process")
    se.get_engine("sname").coupling_relation(pro_name, "generator", gen_name,
                                             "start")

se.get_engine("sname").insert_external_event("start", None)
model_time = datetime.datetime.now()
end = model_time - Start_time
print(f"model_running_time :{end}\n")
se.get_engine("sname").simulate()
