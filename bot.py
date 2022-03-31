import telebot
from telebot import types
import random
from main import FILE_NAME

bot = telebot.TeleBot('5186365102:AAH__a3Ni8321hddfYIxmc-XFOBZ3bIuIIY')

f = open('test.csv', 'r', encoding='UTF-8')
FILE_NAME.test = f.read().split('\n')
f.close()


cost = ''
country = ''


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("200-300$")
    item2 = types.KeyboardButton("300-400$")
    item3 = types.KeyboardButton('500-700$')
    item4 = types.KeyboardButton('700+$')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(m.chat.id, 'Приветствую в боте поиска горящих путевок. для начала выбери стоймость',
                     reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global cost
    cost = message.text

    if message.text.strip() == '200-300$':
        bot.register_next_step_handler(message, handle_text2)

    elif message.text.strip() == '300-400$':
        bot.register_next_step_handler(message, handle_text2)

    elif message.text.strip() == '500-700$':
        bot.register_next_step_handler(message, handle_text2)

    elif message.text.strip() == '700+$':

        bot.register_next_step_handler(message, handle_text2)

    else:
        return handle_text

    bot.register_next_step_handler(message, handle_text2)

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item12 = types.KeyboardButton('Египет')
    item22 = types.KeyboardButton('Турция')
    item32 = types.KeyboardButton('ОАЭ')

    markup2.add(item12)
    markup2.add(item22)
    markup2.add(item32)

    bot.send_message(message.from_user.id, 'в какую страну поедем?', reply_markup=markup2)


def handle_text2(message):
    global country
    country = message.text
    if country.strip() == 'Египет':
        bot.register_next_step_handler(message, callback_worker)

    elif country.strip() == 'Турция':
        bot.register_next_step_handler(message, callback_worker)

    elif country.strip() == 'ОАЭ':
        bot.register_next_step_handler(message, callback_worker)

    else:
        return handle_text2

    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)

    question = 'примерно за' + str(cost) + ' хчешь поехать в  ' + country + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id,
                         'лови актуальные ссылки : \n' + random.choice(test) + '\n для новго поиска напиши /start')
    elif call.data == "no":
        return callback_worker


# Запускаем бота
bot.polling(none_stop=True, interval=0)