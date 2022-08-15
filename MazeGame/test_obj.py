import os
import time
from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *


class Object(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name, i):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)
        self.insert_input_port("object")
        self.con = i
    
    def ext_trans(self, port, msg):
        print("[object][start]")
        if port == "object":
            print(f"[object][In] {self.get_cur_state()}")
            self._cur_state = "MOVE"
    
    def output(self):
        
        print(f"[object][Out]{self.get_cur_state()}")
        NUM_OBJECT = 10001
        path = "C:/evsim/object"
        os.makedirs(path, exist_ok = True)
        
        
        filename = path + "/object" + str(self.con) + ".txt"
        outfile = open(filename, "w")
        for i in range(1, NUM_OBJECT):
                outfile.write("%d\n" %i)

        outfile.close()
        end_time = time.time()
        Total_time = end_time - start_time
        print("Total Time: " + str(Total_time) + " sec")

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

# System Simulator Initialization
se = SystemSimulator()

start_time = time.time()

se.register_engine("sname", "VIRTURE_TIME", 1)

se.get_engine("sname").insert_input_port("object")
obj_list = list()
for i in range(1, 1000):
    obj = Object(0, Infinite, "obj", "sname", i)
    obj_list.append(obj)

for i in range(1, 1000):
    se.get_engine("sname").register_entity(obj_list[i-1]) 

for i in range(1, 1000):
    se.get_engine("sname").coupling_relation(None, "object", obj_list[i-1], "object")

se.get_engine("sname").insert_external_event("object", None)

se.get_engine("sname").simulate()  #게임시작