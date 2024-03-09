import telebot
import webbrowser
from googletrans import Translator, constants
from time import time
import psutil

import data
from data import tokenbot
from data import recent
translator = Translator()
bot=telebot.TeleBot(tokenbot)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hi!')
    bot.send_message(message.chat.id, f'<Доступные команды> \n/translate - Режим переводчика\n/calc - Режим калькулятора\n/help - Помощь')
    with open('logs.txt', 'a', encoding='utf-8') as logs:
        logs.write(f'\nПрописано /start')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,f'<Доступные команды> \n/translate - Режим переводчика\n/calc - Режим калькулятора\n/help - Помощь')

@bot.message_handler(commands=['calc'])
def calculator1(message):
    bot.send_message(message.chat.id, 'Бот переведен в режим калькулятора')
    bot.send_message(message.chat.id, 'Введи пример для решения без пробелов')
    bot.register_next_step_handler(message, calculator2) 

def calculator2(message):
    digittextcalc = message.text
    try:
        if digittextcalc.isalpha() == True:
            bot.send_message(message.chat.id, f"Error, please try again\nДля повторной попытки введите /calc")
        elif message.text == '/back':
            bot.send_message(message.chat.id, 'Принято')
        else:
            bot.register_next_step_handler(message, calculator2)
            def calcumain():
                start = time()
                usertxt = message.text
                resultcalc = eval(usertxt)
                bot.send_message(message.chat.id, f'{usertxt}={resultcalc}')
                print(f'Время ответа - {format(time() - start)[:4]}')
            calcumain()
    except:
        bot.send_message(message.chat.id, f'Unexpected error, please try again')
        calculator1

@bot.message_handler(commands=['translate'])
def calc(message):
    bot.send_message(message.chat.id,'Бот переведен в режим переводчика')
    bot.send_message(message.chat.id, 'Введи текст для перевода')
    bot.register_next_step_handler(message, translate)
def translate(message):
    if message.text == "/back":
        bot.send_message(message.chat.id, 'Принято')
    else:
        bot.register_next_step_handler(message, translate)
        def translatetwo():
            start = time()
            translation = translator.translate({message.text})
            a = f'{translation.origin}'
            b = f'{translation.src}'
            c = f'{translation.text}'
            d = f'{translation.dest}'
            bot.send_message(message.chat.id, f" {a[2:][:-2]}  ({b}) --> {c[2:][:-2]} ({d}) \nДля возврата введи /back")
            print(print(f'{message.text} = {translation.text} \n Для возврата введи /back \n Для продолжения /go'))
            print(f'Время ответа - {format(time() - start)[:4]}')
            data.recent = f'{message.text} = {translation.text[2:-2]}'
        translatetwo()

@bot.message_handler(commands=['back'])
def mode(message):
    bot.send_message(message.chat.id, 'Выберите режим')

@bot.message_handler(commands=["recent"])
def recentt(message):
    bot.send_message(message.chat.id, data.recent)





bot.polling(none_stop=True) 
