from game_bot import *

#게임활용의 수업, 운영

# DB 처음으로 생성 후 다시 주석처리
conn = sqlite3.connect("record.db")
with conn:
    cur = conn.cursor()

    cur.execute("CREATE TABLE \
                 game_record(id integer primary key autoincrement, \
                             chat_id integer not null,\
                             try_time not null,\
                             command text not null,\
                             command_result text not null,\
                             remarks);")

    cur.execute("CREATE TABLE \
                map_record(id integer primary key autoincrement, \
                           chat_id integer not null,\
                           map_result);")

    conn.commit()

    
# System Simulpythator Initialization

#시스템시뮬레이터 객체 생성

# 텔레그램 봇 이름 : maze_game_romm(@maze_guide_bot)

game_bot = Bot('VIRTUAL_TIME') #VIRTUAL_TIME,REAL_TIME


# Move.blk('R', 'F')

updater = game_bot.get_updater()

updater.start_polling()
updater.idle()

