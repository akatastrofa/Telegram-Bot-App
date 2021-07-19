import telebot
from creating_force import keys, TOKEN
from leggy_force import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    start_text = 'Вас приветствует бот, подсказывающий курсы валют. \nЧтобы ознакомиться со списком валют, нажмите /find_out. \
\nЧтобы ознакомиться с принципом работы бота, нажмите /help'
    bot.reply_to(message, start_text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    help_text = 'Для начала работы бота введите команду в следующем формате: \n<Имя переводимой валюты>, \
<Имя валюты, в которую переводим>, \
<Количество переводимой валюты> (обязательно через запятую)\nЧтобы ознакомиться со списком валют, нажмите /find_out'
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['find_out'])
def find_out(message: telebot.types.Message):
    find_out_text = 'Список доступных валют. Чем богаты, тем и рады, так сказать.'
    for key in keys.keys():
        find_out_text = '\n'.join((find_out_text, key(l)))
    bot.reply_to(message, find_out_text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    for key in keys:
        while key.lower() == key.upper():
            return True
    try:
        values = message.text.split(', ')

        if len(values) != 3:
            raise ConvertionException('Несоответствие количества параметров. Должно быть 3.')

        quote, base, amount = values
        total_base = CurrencyConverter.converter(quote, base, amount)
        should_count = float(values[2])
        now_it_counts = total_base * should_count
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        converter_text = f'Стоимость {amount} {quote} в {base} составляет {now_it_counts}'
        bot.send_message(message.chat.id, converter_text)

bot.polling()