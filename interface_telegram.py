import telepot
from telepot.loop import MessageLoop
import time

from env import telegram_bot_token

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command

    if command == '/start':
        bot.sendMessage(chat_id, 'welcome')
    elif command == '/hi':
        bot.sendMessage(chat_id, 'hello world')
    elif command == '/clip':
        bot.sendVideo(chat_id, open('/Users/arnaubennassarformenti/Downloads/Volley_Feroe_cut_min38.30.mp4'))
    else:
        bot.sendMessage(chat_id, 'say what?')

bot = telepot.Bot(telegram_bot_token)

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

while 1:
    time.sleep(10)
