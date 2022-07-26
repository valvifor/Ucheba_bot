

# 2090356465:AAF7J9Rr7jJLKpp81MIwa2Y7bIR-gadfLYM
#TOKEN = '2090356465:AAF7J9Rr7jJLKpp81MIwa2Y7bIR-gadfLYM'

# -*- coding: utf-8 -*-

import telebot
from telebot import types
from datetime import datetime
from threading import Thread

from commands import Command
from keyboard import Keyboard

from all_json_data import *

@Main.BOT.message_handler(content_types=["text"])
def get_message(message):
    print("%s : %s : %s" % (datetime.now(), message.chat.id, message.text))
    Command.get_answer(message.chat.id, message.text)


@Main.BOT.callback_query_handler(func=lambda call: True)
def query_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    call_data = call.data.split("/")

    print("%s : %s : %s" % (datetime.now(), chat_id, call_data))

    if not chat_id in Main.USER_LIST:
        Main.USER_LIST[chat_id] = {"dir": "menu"}

    try:
        if call_data[0] == "menu":
            Keyboard.menu_keyboard(chat_id, None, message_id)

        elif call_data[0] == "admin":
            admin_commands[call_data[1]](chat_id)

        elif call_data[0] == "rules":
            if len(call_data) <= 2:
                Keyboard.rules_keyboard(chat_id, call_data, message_id)
            else:
                send_rule = Rule()
                Thread(target=send_rule.send_file, args=(chat_id, call_data)).start()

        elif call_data[0] in all_lessons and len(call_data) == 1:
            Keyboard.lesson_keyboard(chat_id, call_data[0], message_id)

        elif call_data[1] in all_lessons[call_data[0]]["more"]:
            Main.USER_LIST[chat_id]["dir"] = "/".join(call_data)
            all_lessons[call_data[0]]["more"][call_data[1]]["func"](chat_id)

    except Exception as error:
        print(error)


if __name__ == "__main__":
    Main.START_TIME = datetime.now()
    Main.BOT.polling(none_stop=True)