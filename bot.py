import random

import telebot
from telebot import types
from parcer import parser
import database

bot = telebot.TeleBot('5186365102:AAH__a3Ni8321hddfYIxmc-XFOBZ3bIuIIY')

f = open('test.csv', 'r', encoding='UTF-8')
test = f.read().split('\n')
f.close()

costables = ['200-400', '400-600', '600-700', '>700']
countryees = ['Египет', "ОАЭ", "Турция"]
days = ['5-7', '8-11', '12-15', '>16']
qwes = ['yes', 'no']

@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == '/start':
        global country
        country = message.text
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)
        for costable in costables:
            bth = types.InlineKeyboardButton(costable, callback_data='costables')
            markup.add(bth)
        bot.send_message(user_id, """добро пожаловать в бот поиска горящих путевок. 
        для начала выбери цену в долларах""", reply_markup=markup)
        bot.register_next_step_handler(message, handle_text)
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        database.set_users(user_id, username, first_name, last_name)
    else:
        bot.send_message(message.from_user.id, 'напиши /start что бы начать')

@bot.message_handler(func=lambda message: True, content_types=['button'])

def handle_text(message):
    global cost
    cost = message.text
    costy = message.from_user.id
    markup2 = types.InlineKeyboardMarkup(row_width=2)
    for countryee in countryees:
        btn2 = types.InlineKeyboardButton(countryee, callback_data=countryee)
        markup2.add(btn2)
    bot.send_message(costy, 'теперь можем выбрать страну', reply_markup=markup2)
    bot.register_next_step_handler(message, markups)




def markups(message):
    global daysy
    daysy = message.text
    user_id = message.from_user.id
    markup3 = types.InlineKeyboardMarkup(row_width=1)
    for day in days:
        btn3 = types.InlineKeyboardButton(day, callback_data=day)
        markup3.add(btn3)
    bot.send_message(user_id, 'на сколько ночей хочешь уехать?', reply_markup=markup3)
    bot.register_next_step_handler(message, quest)

def quest(message):
    global dd
    dd = message.text
    markup4 = types.InlineKeyboardMarkup(row_width=2)
    for qwe in qwes:
        btn4 = types.InlineKeyboardButton(qwe, callback_data=qwe)
        markup4.add(btn4)
    question = 'примерно за ' + str(cost) + ' хoчешь поехать в  ' + daysy + " на " + dd + ' дней?'
    bot.send_message(message.from_user.id, text=question, reply_markup=markup4)

@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    if call.data == "yes":
        answer = parser()
        bot.send_message(call.message.chat.id, 'лови актуальные предложения : \n'
                         + str(random.choice(answer['title']))
                         + str(answer['costdoll'])
                         + str(random.choice(answer['countrygo']))
                         + str(random.choice(answer['whenfly']))
                         + str(random.choice(answer['href'])))
        bot.send_message(call.message.chat.id, 'для новго поиска напиши /start')
    elif call.data == "no":
        return callback_worker


bot.polling()