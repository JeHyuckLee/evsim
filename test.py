import telegram

chat_token = "5270412803:AAHU6RCPczvA_lBW1lgiVvFKcZiSABysGvs"
chat = telegram.Bot(token = chat_token)
updates = chat.getUpdates()
for u in updates:
    print(u.message['chat']['id'])