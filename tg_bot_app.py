import telebot
from keys_and_token import keys, TOKEN
from exc_classes import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    start_text = 'Вас приветствует бот, подсказывающий курсы валют. \
\nДля начала работы бота введите команду в следующем формате: \n<Имя переводимой валюты>, \
<Имя валюты, в которую переводим>, \
<Количество переводимой валюты> (обязательно через запятую)\
\n\nНажмите /find_out чтобы ознакомиться со списком валют, .\
 \n\nНажмите /help, чтобы получить порцию моральной поддержки от бота!'
    bot.reply_to(message, start_text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    help_text = 'У тебя всё получится!\
\nПросто введи название переводимой валюты, затем поставь запятую, напиши название валюты, в которую хотелось бы перевести, \
снова поставь запятую и напиши количество переводимой валюты.\
\n\nНапример: доллар, рубль, 100. В результате ты узнает, сколько будут стоить 100 долларов в рублях.\
\n\nНу, а, чтобы узнать список доступных валют, просто вызови команду /find_out.\
\nДерзай! Смотреть курсы валют очень весело :D'
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['find_out'])
def find_out(message: telebot.types.Message):
    find_out_text = 'Список доступных валют. Чем богаты, тем и рады, так сказать.'
    for key in keys.keys():
        find_out_text = '\n— '.join((find_out_text, key))
    bot.reply_to(message, find_out_text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(', ') #Разделяем валюты запятой, так как название валюты может быть из двух слов

        if len(values) != 3:
            raise ConvertionException('Несоответствие количества параметров. Должно быть 3.')

        quote, base, amount = map(lambda x: x.lower(), values) #Регистр букв не имеет значения при вводе
        total_base = CurrencyConverter.converter(quote, base, amount)
        should_count = float(values[2])
        now_it_counts = total_base * should_count #Приводим в действие переменную 'amount'
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        converter_text = f'Стоимость {amount} {quote} в {base} составляет {now_it_counts}'
        bot.send_message(message.chat.id, converter_text)

bot.polling()
