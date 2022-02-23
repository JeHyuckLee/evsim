from pydoc import describe
from tabnanny import check
from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from random import *
import datetime
import math
import time

import matplotlib.pyplot as plt


class Point:

    def __init__(self, cX, cY):

        #현재위치
        self.current_x = cX
        self.current_y = cY
        #시각화를 위한 리스트
        self.listX = []
        self.listY = []


class Move(Point):

    def __init__(self, cX, cY):
        Point.__init__(self, cX, cY)
        self.epsilon = 0.000000001

    # 대각선 이동
    def update(self, dX, dY, v=1):
        #목적지
        self.destination_x = dX
        self.destination_y = dY

        #각도
        self.degrees = math.atan2(self.destination_y - self.current_y,
                                  self.destination_x - self.current_x)
        print(f"atan2: {self.degrees}")

        # 대각선 이동을 위한 계산
        if self.current_x < self.destination_x - v and self.current_y < self.destination_y - v:
            self.current_x += math.cos(self.degrees) * v
            self.current_y += math.sin(self.degrees) * v
            print(
                f"distance: {math.sqrt(math.cos(self.degrees)**2+math.sin(self.degrees)**2)}\n"
            )
        else:
            # 나머지 계산
            remainder_X = self.destination_x - self.current_x
            remainder_Y = self.destination_y - self.current_y
            re_distance = math.sqrt(remainder_X**2 + remainder_Y**2)

            if re_distance >= v:
                self.current_x += math.cos(self.degrees) * v
                self.current_y += math.sin(self.degrees) * v
                print(
                    f"distance: {math.sqrt(math.cos(self.degrees)**2+math.sin(self.degrees)**2)}\n"
                )
            else:
                self.current_x += remainder_X
                self.current_y += remainder_Y
                print(
                    f"distance: {math.sqrt(remainder_X**2+remainder_Y**2)}\n")

        self.listX.append(self.current_x)
        self.listY.append(self.current_y)


# 직선 이동

    def straight_update(self, dX, dY, v=1):
        self.destination_x = dX
        self.destination_y = dY

        if (self.current_x < self.destination_x - v):
            self.current_x += v
        elif (self.current_x < self.destination_x):
            remainder = self.destination_x - self.current_x
            self.current_x += remainder
        elif (self.current_x == self.destination_x
              and self.current_y < self.destination_y - v):
            self.current_y += v
        else:
            remainder = self.destination_y - self.current_y
            self.current_y += remainder

    #입실론
    def check(self, dx, dy):
        if (dx - self.epsilon < self.current_x < dx + self.epsilon
                and dy - self.epsilon < self.current_y < dy + self.epsilon):
            return True
        else:
            return False


class Generator(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name, X, Y,
                 number):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 0.1)

        self.insert_input_port("start")

        #도착지점 랜덤생성
        self.destination_x = uniform(-10, 10)
        self.destination_y = uniform(-10, 10)

        #도착지가 랜덤으로 변하는횟수
        self.count = 0
        self.number_of_repetitions = number

        self.move = Move(X, Y)

    def ext_trans(self, port, msg):
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"

    def output(self):
        print(f"[Gen][OUT]: {datetime.datetime.now()}\n")

        #목적지에 도착한걸 확인한 경우 다시 목적지를 새로 랜덤으로 생성
        if (self.destination_y == self.move.current_y
                and self.destination_x == self.move.current_x
                and self.move.check(self.destination_x, self.destination_y)):

            self.destination_x = uniform(-10, 10)
            self.destination_y = uniform(-10, 10)
            self.count += 1

        #목적지로 이동
        else:
            self.move.update(self.destination_x, self.destination_y)
            print(f"cX: {self.move.current_x}, cY: {self.move.current_y}")
            print(
                f"dX: {self.move.destination_x}, dY: {self.move.destination_y}\n"
            )

        #시각화 파트
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.plot(self.move.listX, self.move.listY, 'ro--', linewidth=3)
        plt.draw()
        plt.pause(0.1)
        plt.cla()
        return None

    def int_trans(self):
        #반복횟수를 다채우면 종료
        if self._cur_state == "MOVE" and self.number_of_repetitions == self.count:
            self._cur_state = "IDLE"

            # 시각화

        else:
            self._cur_state = "MOVE"


# System Simulator Initialization

se = SystemSimulator()  #게임엔진

se.register_engine("sname", "VIRTUAL_TIME", 0.1)
#sname = 로비창, 공간? ,방,  real_time 실시간 , 0.1 시간의 해상도 0.1 => 1초를 0.1초 단위로 잰다. realtime일때 의미가있음
#VIRTUAL_TIME 처리하는대로
#mininumtime에 맞아야한다.
se.get_engine("sname").insert_input_port("start")

gen = Generator(0, Infinite, "Gen", "sname", 0, 0, 10)
#0 -> 생성시간 , Infinite -> 소멸시간, "Gen" 엔진의 이름 , "sname" 속한곳,

se.get_engine("sname").register_entity(gen)  #공간을 가져와서

se.get_engine("sname").coupling_relation(None, "start", gen, "start")  #개체를 등록
#None -> se
#모델간의 연결

se.get_engine("sname").insert_external_event("start", None)  #이벤트 발생시 다른스레드 에게
#외부입력을 start 포트에 msg를(none)
#none-> 이벤트 트리거

#스레드가 키보드입력을 받으면 insert_external_event로 꽂아준다

se.get_engine("sname").simulate()  #blocking

#주석 , 수정
#변수 이름
#코디네이션
#zero mq, MQTT -> 이벤트를 원격으로 처리 프로세스 통신 , 멀티user를 지원,
#사용자입력 + 엔진 의 연결
#파이게임?
#외부에서 입력이 있을때만 동작
#idel -> 외부에서 입력 -> Move 사용자로부터입력을 받아야한다.
#멀티스레드
# 엔진에서 스레드 x 모델에서 키보드입력을 체크
# 키보드처리하는 모델을 추가 mqtt에서 키보드처리 하는것을 만들어서 꽂아준다.

#TASK : Zero mq, MqTT 스터디,, 담주 붙여본다. example 로 코딩을한번 해보
#mqtt  구독
#zeromq p2p
#필요할때 메세지 보내고 처리..하고
