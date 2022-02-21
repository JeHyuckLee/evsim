from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime
import math

import matplotlib.pyplot as plt


class Generator(BehaviorModelExecutor):

    def __init__(self,
                 instance_time,
                 destruct_time,
                 name,
                 engine_name,
                 X,
                 Y,
                 dia=True):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("start")

        self.dia = dia  #데코레이터, 클래스확장
        self.X = X  #destination
        self.Y = Y
        self.distance = 0
        self.distance_x = 0
        self.distance_y = 0
        self.listX = []
        self.listY = []

        # 목표 지점까지의 각도 계산
        self.degrees = math.atan2(self.Y, self.X)

    def ext_trans(self, port, msg):
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"

    def output(self):
        print(f"[Gen][OUT]: {datetime.datetime.now()}")

        # 속력
        v = 1
        if self.distance >= 5:
            v = 2

        # 대각선이동, 직선이동
        if (self.dia):
            self.update(v)
        else:
            self.straight_update(v)

        # 시각화를 위한 리스트
        self.listX.append(self.distance_x)
        self.listY.append(self.distance_y)

        return None

    def int_trans(self):
        if self._cur_state == "MOVE" and self.distance_x == self.X and self.distance_y == self.Y:
            self._cur_state = "IDLE"

            # 시각화
            plt.plot(self.listX, self.listY, 'ro--', linewidth=2)
            plt.show()
        else:
            self._cur_state = "MOVE"

    # 대각선 이동
    def update(self, v=1):

        # 대각선 이동을 위한 계산
        if self.distance_x < self.X - v and self.distance_y < self.Y - v:
            self.distance_x += math.cos(self.degrees) * v
            self.distance_y += math.sin(self.degrees) * v
        else:
            # 나머지 계산
            remainder_X = self.X - self.distance_x
            remainder_Y = self.Y - self.distance_y
            re_distance = math.sqrt(remainder_X**2 + remainder_Y**2)

            if re_distance >= v:
                self.distance_x += math.cos(self.degrees) * v
                self.distance_y += math.sin(self.degrees) * v
            else:
                self.distance_x += remainder_X
                self.distance_y += remainder_Y

        # 총 이동한 거리 계산
        self.distance = math.sqrt(self.distance_x**2 + self.distance_y**2)

        print(f"X: {self.distance_x}, Y: {self.distance_y}")

        print("진행한 거리: %.1f" % self.distance)  #영어

    # 직선 이동
    def straight_update(self, v=1):

        if (self.distance_x < self.X - v):
            self.distance_x += v
        elif (self.distance_x < self.X):
            remainder = self.X - self.distance_x
            self.distance_x += remainder
        elif (self.distance_x == self.X and self.distance_y < self.Y - v):
            self.distance_y += v
        else:
            remainder = self.Y - self.distance_y
            self.distance_y += remainder

        # 총 이동한 거리 계산
        self.distance = self.distance_x + self.distance_y
        print(f"X: {self.distance_x}, Y: {self.distance_y}")

        print("진행한 거리: %.1f" % self.distance)


# System Simulator Initialization

se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("start")

gen = Generator(0, Infinite, "Gen", "sname", 10,
                10)  # True = 대각선이동 , False = 가로 -> 세로 이동

se.get_engine("sname").register_entity(gen)

se.get_engine("sname").coupling_relation(None, "start", gen, "start")

se.get_engine("sname").insert_external_event("start", None)

se.get_engine("sname").simulate()