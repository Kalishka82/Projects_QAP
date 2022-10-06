import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username}!\
    \nНужна помощь в конвертации валют? Я помогу \
    \n \
    \nВведите через пробел: \
    \nимя валюты для перевода (имя из 2х слов вводить слитно) \
    \nимя валюты, в которую хотите перевести \
    \nколичество переводимой валюты \
    \n \
    \nПосмотреть список всех доступных валют: /values \
    \nНужна помощь? нажмите /help') 


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'введите через пробел: \nимя валюты для перевода (имя из 2х слов вводить слитно) \
\nимя валюты, в которую хотите перевести \
\nколичество переводимой валюты \
\n \
\nПосмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().replace(',', '.').split(' ')

        if len(values) != 3:
            raise APIException('Не совпадает количество введенных параметров\
            \nДля помощи нажмите /help')
        
        quote, base, amount = values 
        total = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {round(total, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
