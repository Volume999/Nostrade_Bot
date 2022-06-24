import telebot
import yaml

COMMAND_WIDTH = 1
COMMANDS = [["Today's Forecast"],
            ["Week Forecast"],
            ["Year Forecast"],
            ["Options"]]

OPTIONS_WIDTH = 1
OPTIONS = [
    ["Settings"],
    ["Subscribe"],
    ["About"]
]

FORECAST_RECIPIENT_WIDTH = 1
FORECAST_RECIPIENTS = [
    "Your sign",
    "Other sign"
]
with open('config.yaml') as f:
    settings = yaml.load(f, Loader=yaml.loader.SafeLoader)

mode = None

bot = telebot.TeleBot(settings['bot_api_key'])


# React to /start, /help
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=COMMAND_WIDTH)
    for row in COMMANDS:
        markup.add(*row)
    bot.send_message(message.chat.id, "Choose Mode", reply_markup=markup)


# React to clicking inline buttons
@bot.callback_query_handler(func=lambda call: call.data == '1')
def handle_callback_query(call):
    help(call)
    bot.answer_callback_query(call.id, text='Received!')
    bot.send_message(call.message.chat.id, "Hi!")


def show_options(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=OPTIONS_WIDTH)
    for row in OPTIONS:
        markup.add(*[telebot.types.InlineKeyboardButton(option, callback_data=option) for option in row])
    bot.send_message(message.chat.id, "Choose Option", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in FORECAST_RECIPIENTS)
def show_forecast(call):
    bot.send_message(call.message.chat.id, f"Showing forecast for {mode} for {call.message.chat.username}")


def select_recipient(message, forecast_mode):
    global mode
    mode = forecast_mode
    markup = telebot.types.InlineKeyboardMarkup(row_width=FORECAST_RECIPIENT_WIDTH)
    markup.add(
        *[telebot.types.InlineKeyboardButton(recipient, callback_data=recipient) for recipient in FORECAST_RECIPIENTS])
    bot.send_message(message.chat.id, "Which sign do you want a forecast for?", reply_markup=markup)


@bot.message_handler()
def handle_mode_select(message):
    match message.text:
        case "Options":
            print("Showing Options")
            show_options(message)
        case "Today's Forecast":
            select_recipient(message, forecast_mode="Today")
        case "Week Forecast":
            select_recipient(message, forecast_mode="Week")
        case "Year Forecast":
            select_recipient(message, forecast_mode="Year")
    print(message.text, "selected")


bot.polling()
