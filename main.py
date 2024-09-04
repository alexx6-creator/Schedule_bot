import telebot
import time
import json
from datetime import datetime
from cfg import *

bot=telebot.TeleBot(Api)

#Считывание данных с файла с Расписанием( "Schedule.json" )
with open('Schedule.json', 'r', encoding='utf-8') as file:
    schedule = json.load(file)

# Функция для сравнения времени
def time_in_range(start, end, current):
    return start <= current <= end

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"Я - бот расписание. Напиши /para для просмотра текущей и следующей пары")

@bot.message_handler(commands=['para'])
def para(message):
    # Определяем текущую и следующую пару
    current_period = None
    next_period = None

    # Получаем текущий день недели (например, 'monday')
    day_of_week = datetime.now().strftime('%A').lower()

    # Получаем текущее время
    current_time = datetime.now().time()

    for period, details in schedule[day_of_week].items():
        start_time_str, end_time_str = details[2].split(' - ')
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        if time_in_range(start_time, end_time, current_time):
            current_period = details
        elif current_time < start_time and not next_period:
            next_period = details

    # Вывод информации о текущей и следующей паре
    if current_period:
        bot.reply_to(message,f'Текущая пара: {current_period[0]},\nКабинет: {current_period[1]}')
    else:
        bot.reply_to(message,'Сейчас нет пары.')

    if next_period:
        st_time = start_time.strftime('%H:%M')
        bot.reply_to(message,f'Следующая пара: {next_period[0]},\nКабинет: {next_period[1]},\nНачало пары в: {st_time}')
    else:
        bot.reply_to(message,'Сегодня больше пар нет.')
        
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Извините, я понимаю только команды /start и /para.")

if __name__=='__main__':
    bot.polling()