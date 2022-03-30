import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

##기존 코드
from cmath import sqrt
from concurrent.futures.process import _check_system_limits
from dis import Instruction
from doctest import FAIL_FAST
from msilib.schema import SelfReg

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from Agent import *
from Game_manager import *

#게임활용의 수업, 운영
class command_list():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.cm_list = list()

        self.rblk_cm = ''
        self.lblk_cm = ''
        self.fblk_cm = ''
        self.bblk_cm = ''

    def R(self):
        self.cm_list.append('R')

    def L(self):
        self.cm_list.append('L')

    def F(self):
        self.cm_list.append('F')

    def B(self):
        self.cm_list.append('B')

    def Blk(self, blk, cm):
        if blk == 'R':
            self.rblk_cm = cm
        elif blk == 'L':
            self.lblk_cm = cm
        elif blk == 'F':
            self.fblk_cm = cm
        elif blk == 'B':
            self.bblk_cm = cm

    def get_blk(self, blk):
        if blk == 'R':
            return self.rblk_cm
        elif blk == 'L':
            return self.lblk_cm
        elif blk == 'F':
            return self.fblk_cm
        elif blk == 'B':
            return self.bblk_cm

    def get_command(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.cm_list


# System Simulator Initialization

se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("command")

gm = Gamemanager(0, Infinite, "gm", "sname")
se.get_engine("sname").register_entity(gm)

agent = Agent(0, Infinite, "agent", "sname", 1, 1)  #에이전트의 시작위치 지정
se.get_engine("sname").register_entity(agent)

se.get_engine("sname").coupling_relation(None, "command", agent, "command")

se.get_engine("sname").coupling_relation(agent, "gm", gm, "agent")
se.get_engine("sname").coupling_relation(gm, "agent", agent, "gm")

Move = command_list()

# 명령어 파트 시작
# 텔레그램 봇 이름 : maze_game_romm(@maze_guide_bot)
BOT_TOKEN='5270412803:AAHU6RCPczvA_lBW1lgiVvFKcZiSABysGvs'
 
updater = Updater( token=BOT_TOKEN, use_context=True )
dispatcher = updater.dispatcher

Move.Blk('F', 'R')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
    """미로 게임
    /guide : 기본 이동 명령어를 알려줍니다.
    /command 명령어 : 명령어에 따라 리스트에 이동 동작을 추가합니다.
    /list : 추가한 이동 동작 리스트를 출력합니다.
    /reset : 이동 동작 리스트를 초기화합니다.
    /simulation : 추가한 이동 동작 리스트에 따라 동작을 수행합니다.""".format(map))


def list(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="[{}]".format(Move.cm_list))

def reset(update, context):
    Move.cm_list.clear()
    context.bot.send_message(chat_id=update.effective_chat.id, text="리스트 초기화 완료")

def guide(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
    """가이드
    Move.방향()을 활용하여 파이썬 코드를 작성합니다.
    방향은 F(앞), B(뒤), L(좌), R(우)으로 지정할 수 있습니다.
    """)

def command(update, context):
    com = context.args[0]
    for i in range(1,len(context.args)):
        com = com + ' '+ context.args[i]
    try :
        exec(format(com))
    except Exception :
        context.bot.send_message(chat_id=update.effective_chat.id, text="잘못된 문법입니다.")
    else :
        context.bot.send_message(chat_id=update.effective_chat.id, text="다음의 명령을 추가합니다. : {} ".format( com ))


def simulation(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="이동을 시작합니다.")
    if Move.get_blk('R') != None:
        agent.Set_Ifmove('R', Move.get_blk('R'))
    if Move.get_blk('L') != None:
        agent.Set_Ifmove('L', Move.get_blk('L'))
    if Move.get_blk('F') != None:
        agent.Set_Ifmove('F', Move.get_blk('F'))
    if Move.get_blk('B') != None:
        agent.Set_Ifmove('B', Move.get_blk('B'))

    se.get_engine("sname").insert_external_event("command", Move.get_command())
    se.get_engine("sname").simulate()

start_handler = CommandHandler('start', start)
guide_handler = CommandHandler('guide', guide)
command_handler = CommandHandler('command', command)
list_handler = CommandHandler('list', list)
reset_handler = CommandHandler('reset', reset)
simulation_handler = CommandHandler('simulation', simulation)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(guide_handler)
dispatcher.add_handler(command_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(reset_handler)
dispatcher.add_handler(simulation_handler)
updater.start_polling()
updater.idle()
