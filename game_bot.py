from Agent import Agent
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

import numpy as np

from system_simulator import SystemSimulator
from Game_manager import *
from command_list import *


class Bot():
    updater = Updater( token='5270412803:AAHU6RCPczvA_lBW1lgiVvFKcZiSABysGvs', use_context=True ) #자신의 봇 토큰 
    dispatcher = updater.dispatcher

    def __init__(self, mode):
        self.agents = {}
        self.gm = Gamemanager(0, Infinite, "gm", "sname")
        self.mode = mode
        self.method_list = {
            'start' : self.start,
            'guide' : self.guide,
            'command' : self.command,
            'location' : self.location,
            'list' : self.list,
            'reset' : self.reset,
            'simulation' : self.simulation,
            'register' : self.register
        }

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        """미로 게임
        /register : Agent를 등록합니다. 
        /guide : 기본 이동 명령어를 알려줍니다.
        /command 명령어 : 명령어에 따라 리스트에 이동 동작을 추가합니다.
        /location : 캐릭터의 현재 위치를 출력합니다.
        /list : 추가한 이동 동작 리스트를 출력합니다.
        /reset : 이동 동작 리스트를 초기화합니다.
        /simulation : 추가한 이동 동작 리스트에 따라 동작을 수행합니다.""")

    def register(self, update, context):
        user = context.args[0]
        chat_id = update.effective_chat.id
        exec("{} = command_list()".format(user),globals())
        if user in self.agents.keys() : 
            if chat_id not in self.agents[user].chat_id : 
                self.agents[user].chat_id.append(chat_id)
                context.bot.send_message(chat_id=update.effective_chat.id, text="사용자 등록합니다.")
            else :
                context.bot.send_message(chat_id=update.effective_chat.id, text="이미 등록된 사용자입니다.")
        else :
            self.agents[user]=Agent(0, Infinite, "agent", "sname", 1, 1, self.updater.bot)
            self.agents[user].chat_id.append(chat_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Agent를 등록합니다.")
    

    def guide(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        """가이드
        Move.방향()을 활용하여 파이썬 코드를 작성합니다.
        방향은 F(앞), B(뒤), L(좌), R(우)으로 지정할 수 있습니다.
        """)

    def command(self, update, context):
        com = context.args[0]
        for i in range(1,len(context.args)):
            com = com + ' '+ context.args[i]
        try :
            exec(format(com))
        except Exception :
            context.bot.send_message(chat_id=update.effective_chat.id, text="잘못된 문법입니다.")
        else :
            context.bot.send_message(chat_id=update.effective_chat.id, text="다음의 명령을 추가합니다. : {} ".format( com ))

    def list(self, update, context):
        user = context.args[0]
        exec("command = {}.cm_list".format(user), None, locals())
        context.bot.send_message(chat_id=update.effective_chat.id, text="[{}]".format(locals()['command']))

    def location(self, update, context):
        user = context.args[0]
        try :
            agent = self.agents[user]
            Fog = [[8 for col in range(18)] for row in range(18)]
            for j in range(agent.ix-1, agent.ix+2):
                for i in range(agent.iy-1, agent.iy+2):
                    Fog[i][j] = map[i][j]
            Fog[agent.iy][agent.ix] = 5
            context.bot.send_message(chat_id=update.effective_chat.id, text="{}".format(np.array(Fog)))
        except Exception :
            context.bot.send_message(chat_id=update.effective_chat.id, text="Agent가 존재하지 않습니다..")


    def reset(self, update, context):
        user = context.args[0]
        exec("{}.cm_list.clear()".format(user))
        context.bot.send_message(chat_id=update.effective_chat.id, text="리스트 초기화 완료")

    def simulation(self, update, context):
        user = context.args[0]
        try:
            agent = self.agents[user]
        except :
            context.bot.send_message(chat_id=update.effective_chat.id, text="Agent가 존재하지 않습니다.")
        else : 
            simulator = SystemSimulator()
            simulator.register_engine("sname", self.mode, 0.01) 
            simulator.get_engine("sname").insert_input_port("command")
            
            simulator.get_engine("sname").register_entity(self.gm)
            simulator.get_engine("sname").register_entity(agent)


            simulator.get_engine("sname").coupling_relation(None, "command", agent, "command")
            simulator.get_engine("sname").coupling_relation(agent, "gm", self.gm, "agent")
            simulator.get_engine("sname").coupling_relation(self.gm, "agent", agent, "gm")

            if globals()[user].get_blk('R') != None:
                agent.Set_Ifmove('R', globals()[user].get_blk('R'))
            if globals()[user].get_blk('L') != None:
                agent.Set_Ifmove('L', globals()[user].get_blk('L'))
            if globals()[user].get_blk('F') != None:
                agent.Set_Ifmove('F', globals()[user].get_blk('F'))
            if globals()[user].get_blk('B') != None:
                agent.Set_Ifmove('B', globals()[user].get_blk('B'))
            
            exec("command = {}.get_command()".format(user),None,locals())
            context.bot.send_message(chat_id=update.effective_chat.id, text="이동을 시작합니다.")
            simulator.get_engine("sname").insert_external_event("command", locals()["command"])
            if self.mode == "VIRTUAL_TIME":
                simulator.get_engine("sname").simulate()
            else : 
                simulator.get_engine("sname").simulate(len(locals()["command"])*1.2)
            context.bot.send_message(chat_id=update.effective_chat.id, text="시뮬레이션을 종료합니다.")
            del simulator
        

    def get_updater(self):
        for name in self.method_list.keys():
            self.dispatcher.add_handler(CommandHandler(name, self.method_list[name]))

        return self.updater
