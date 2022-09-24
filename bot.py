import os

import telebot
from telebot import types  # для указание типов
import config
import functions
import plotly

bot = telebot.TeleBot(config.TOKEN)

connection = functions.create_connection("C:\sqlite\database.db")

select_users = "SELECT * from request_daily"
users = functions.execute_read_query(connection, select_users)

users_text = ""

for a in users:
    for b in a:
        users_text += str(b) + " "
last_name, first_name = "", ""  # Зададим дефолтные фамилию и имя

print(users_text)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ввести фамилию и имя")
    btn3 = types.KeyboardButton("Дашборд")
    # btn2 = types.KeyboardButton("❓ Задать вопрос")
    btn4 = types.KeyboardButton("Статус")
    markup.add(btn1, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Вас приветствует чат-бот Газпромнефти!".format(
                         message.from_user), reply_markup=markup)


# @bot.message_handler(commands=['text'])
# def get_name(message):


# @bot.message_handler(content_types=['text'])
# def func_base(message):
#     if (message.text == "👋 Поздороваться!!!!!"):
#         bot.send_message(message.chat.id, text=users)


def after_text_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # print('Ваша Ф. И. ', str(message.text).split()[0], str(message.text).split()[1])
    last_name, first_name = str(message.text).split()[0], str(message.text).split()[1]
    file_name = "name_dir/name_" + str(message.from_user.id) + ".txt"
    f = open(file_name, 'w').close()
    with open(file_name, 'w', encoding='utf-8') as f:
        str_tmp = last_name + " " + first_name
        print("IN with open:", str_tmp, last_name, first_name)
        f.write(str_tmp)
        f.close()

    # str_tmp = "Привет, " + last_name + " " + first_name
    str_tmp = "Ваши данные внесены в базу"
    bot.send_message(message.chat.id, text=str_tmp, reply_markup=markup)


def after_text_3(message):
    last_name, first_name = str(message.text).split()[0], str(message.text).split()[1]
    return last_name, first_name


def get_status(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Достаем из базы по req_id status
    connection = functions.create_connection("C:\sqlite\database.db")
    select_users = f"SELECT * FROM request_daily WHERE req_id = {message.text}"
    users = functions.execute_read_query(connection, select_users)

    tmp_str = "Номер закупки   Закупщик   Дата   Этап   Статус" + "\n" + " ".join([str(i) for i in list(users[0])])
    bot.send_message(message.chat.id, text=tmp_str, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    # keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    if message.text == "Ввести фамилию и имя":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.from_user.id, 'Введите вашу фамилию и имя через пробел', reply_markup=markup)
        bot.register_next_step_handler(msg, after_text_2)

    elif (message.text == "Статус"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        file_name = "name_dir/name_" + str(message.from_user.id) + ".txt"
        f = open(file_name, 'r', encoding='utf-8')

        last_name, first_name = f.readline().split()
        print(last_name, first_name)
        f.close()
        if len(last_name) != 0:
            msg = bot.send_message(message.from_user.id, text="Введите номер закупки:", reply_markup=markup)
            bot.register_next_step_handler(msg, get_status)
        else:
            print("Вам необходимо сначала ввести фамилию и имя")

    elif (message.text == "Дашборд"):
        dict_status = {"OK": 0, "RISK": 0, "OVERDUE": 0}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        file_name = "name_dir/name_" + str(message.from_user.id) + ".txt"
        f = open(file_name, 'r', encoding='utf-8')
        last_name, first_name = f.readline().split()
        name_ = str(last_name + " " + first_name)
        str_tmp2 = f'Дашборд для {name_} готов:'
        bot.send_message(message.chat.id, text=str_tmp2, reply_markup=markup)
        connection = functions.create_connection("C:\sqlite\database.db")
        users_name_ = f"SELECT DISTINCT user_name FROM request_daily"
        tmp_ = functions.execute_read_query(connection, users_name_)
        count_OK = f"SELECT count(req_id) FROM request_daily WHERE status = 'OK' and user_name LIKE '%{name_}%'"
        count_RISK = f"SELECT count(req_id) FROM request_daily WHERE status = 'RISK' AND  user_name LIKE '%{name_}%'"
        count_OVERDUE = f"SELECT count(req_id) FROM request_daily WHERE status = 'OVERDUE' AND user_name LIKE '%{name_}%'"

        count_OK_query = functions.execute_read_query(connection, count_OK)
        count_RISK_query = functions.execute_read_query(connection, count_RISK)
        count_OVERDUE_query = functions.execute_read_query(connection, count_OVERDUE)

        print("___________________________________")
        print(count_OK_query, count_RISK_query, count_OVERDUE_query)
        count_list = [count_OK_query[0][0], count_RISK_query[0][0], count_OVERDUE_query[0][0]]
        image_name = "/pic_dir/Image" + str(message.from_user.id) + ".png"

        # os.remove(image_name)
        # functions.plot2(count_list, image_name)

        # image_name = "/pic_dir/Image" + str(message.from_user.id) + ".png"
        # print(image_name)
        # path2 = r"C:\Users\pavel\GazPromTelegramBot\pic_dir\Image" + str(message.from_user.id) + ".png"
        # bot.send_photo(message.chat.id, open(path2, 'rb'))
        bot.send_photo(message.chat.id, open('qwe.png', 'rb'))

        print("___________________________________")
        print()
'''
    elif (message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "У меня нет имени..")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text=users_text)

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
'''

if __name__ == "__main__":
    bot.polling(none_stop=True)
