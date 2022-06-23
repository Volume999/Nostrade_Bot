import telebot
import yaml

COMMAND_WIDTH = 1
COMMANDS = [["Today's Forecast"],
            ["Week Forecast"],
            ["Year Forecast"]]

with open('config.yaml') as f:
    settings = yaml.load(f, Loader=yaml.loader.SafeLoader)

bot = telebot.TeleBot(settings['bot_api_key'])


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    print('Handle start help triggered!')
    bot.reply_to(message, 'Handle triggered!')
    bot.send_message(message.chat.id, 'Handle2')


@bot.message_handler(content_types=['document', 'audio'])
def handle_documents_audio(message):
    print('Handle documents audio triggered!')


@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_textdoc(message):
    print('Handle textdoc triggered!')


@bot.message_handler(commands=['show_buttons'])
def handle_keyboard_buttons(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    markup.add(telebot.types.KeyboardButton(1), telebot.types.KeyboardButton(1), telebot.types.KeyboardButton(1))
    bot.send_message(message.chat.id, "Choose button", reply_markup=markup)


@bot.message_handler(regexp='^1$')
def handle_keyboard_remove_button(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Okay', reply_markup=markup)


@bot.message_handler(commands=['show_inline_buttons'])
def handle_inline_keyboard_buttons(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    markup.add(telebot.types.InlineKeyboardButton("1", callback_data="1"),
               telebot.types.InlineKeyboardButton("1", callback_data="1"),
               telebot.types.InlineKeyboardButton("1", callback_data="1"))
    bot.send_message(message.chat.id, "Choose button", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == '1')
def handle_callback_query(call):
    help(call)
    bot.answer_callback_query(call.id, text='Received!')
    bot.send_message(call.message.chat.id, "Hi!")


bot.polling()
