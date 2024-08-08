from telebot import *
import pandas as pd
import datetime
from telebot.types import ReplyKeyboardMarkup
bot = telebot.TeleBot('7489545535:AAFbTAe92LXW-pyCU8JO7Nl2nKTcUPOISoM')
import csv
import requests

dollars = [{
    'usd': 85,
    'date': '08.08.2024',
}]

df1 = pd.DataFrame(dollars)
df1.to_csv('firstpandas.csv')



def new_usd(new_usd):
    with open('firstpandas.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['usd', 'date'])
        now = datetime.datetime.now()
        csv_writer.writerow([new_usd, now])


def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard



@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я Ракета. Я оставлю тебе Грута, мне надо стырить ногу и лампочки, все я побежал!\n........................")


    bot.send_message(message.chat.id,
                     "Забыл сказать, я научил Грута говорить нынешний курс доллара к рублю. Он тебе скажет только если ты напишешь команду /askgrut", reply_markup=create_keyboard(['/askgroot']))


@bot.message_handler(commands=["askgroot"])
def get_dollar_rub_rate(message):
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)

    # Проверьте код состояния ответа
    if response.status_code != 200:
        raise Exception("Ошибка запроса к API ЦБ РФ")

    # Распакуйте результат
    data = response.json()

    # Получите курс доллара к рублю
    dollar_rub_rate = data["Valute"]["USD"]["Value"]
    new_usd(dollar_rub_rate)

    bot.send_message(message.chat.id, f"Текущий курс доллара к рублю: {dollar_rub_rate:.2f}")
    bot.send_message(message.chat.id, 'Я есть Грут\n/askgroot', reply_markup=create_keyboard(['/askgroot']))

@bot.message_handler(content_types=['text'])
def beleberda(message):
    bot.send_message(message.chat.id, 'Я есть Грут\n/askgroot', reply_markup=create_keyboard(['/askgroot']))


bot.polling()