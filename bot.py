import csv
import telebot
from telebot import types

import database

bot = telebot.TeleBot('5186365102:AAH__a3Ni8321hddfYIxmc-XFOBZ3bIuIIY')

f = open('test.csv', 'r', encoding='UTF-8')
test = f.read().split('\n')
f.close()


countryees = ['Египет', "ОАЭ", "Турция"]
daysy = ['5', '7', '12', '14']
qwes = ['yes', 'no']

markup = types.ReplyKeyboardMarkup(row_width=2)
for cost_able in costables:
    bth = types.InlineKeyboardButton(cost_able, callback_data=cost_able)
    markup.add(bth)

markup2 = types.ReplyKeyboardMarkup(row_width=2)
for countryee in countryees:
    btn2 = types.InlineKeyboardButton(countryee, callback_data=countryee)
    markup2.add(btn2)

markup3 = types.ReplyKeyboardMarkup(row_width=2)
for day in daysy:
    btn3 = types.InlineKeyboardButton(day, callback_data=day)
    markup3.add(btn3)

country = ''
cost = ''
days = ''
dd = ''


@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == '/start':
        user_id = message.from_user.id
        bot.send_message(user_id, """добро пожаловать в бот поиска горящих путевок. 
        для начала напиши максимальную цену в долларах""")
        bot.register_next_step_handler(message, sto_it)
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        database.set_users(user_id, username, first_name, last_name)
    else:
        bot.send_message(message.from_user.id, 'напиши /start что бы начать')


def sto_it(message):

    global costables
    costables = message.text
    costy = message.from_user.id
    bot.send_message(costy, 'теперь можем выбрать страну', reply_markup=markup2)
    bot.register_next_step_handler(message, markupse)

def markupse(message):
    global countryee
    countryee = message.text
    daysys = message.from_user.id
    bot.send_message(daysys, 'на сколько ночей хочешь уехать?', reply_markup=markup3)
    bot.register_next_step_handler(message, quest)

def quest(message):
    global days
    days = message.text
    markup4 = types.ReplyKeyboardMarkup(row_width=2)
    for qwe in qwes:
        btn4 = types.InlineKeyboardButton(qwe, callback_data=qwe)
        markup4.add(btn4)
    question = 'примерно за ' + str(costables) + 'баксов хoчешь поехать в  ' + str(countryee) + " на " + str(days) + ' дней?'
    bot.send_message(message.from_user.id, text=question, reply_markup=markup4)
    bot.register_next_step_handler(message, callback_worker)

@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):
    if call.text == 'yes':
        file = 'test.csv'
        with open(file, "r", encoding='utf-8') as filee:
            reader = csv.reader(filee, delimiter=",")
            next(reader)
            for row in reader:
                f, href, title, costbel, costdoll, countrygo, whenfly, daystrip = row
                if costdoll <= costables and countrygo == countryee and daystrip >= days:

                    bot.send_message(call.from_user.id, f'лови актуальные предложения : \n ,  {", ".join(row)}')
        bot.send_message(call.from_user.id, 'для новго поиска напиши /start')

    elif call.text == "no":
        return start


bot.polling()