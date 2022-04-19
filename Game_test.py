#pythonw -u Game_test.py > log.log 2>&1
#TASKKILL /F /IM pythonw.exe 
from game_bot import *

#게임활용의 수업, 운영

# System Simulpythator Initialization

#시스템시뮬레이터 객체 생성

# 텔레그램 봇 이름 : maze_game_romm(@maze_guide_bot)

game_bot = Bot('VIRTUAL_TIME') #VIRTUAL_TIME,REAL_TIME


# Move.Blk('R', 'F')

updater = game_bot.get_updater()

updater.start_polling()
updater.idle()


