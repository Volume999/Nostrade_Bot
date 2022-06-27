import telebot
import yaml

COMMAND_WIDTH = 1
COMMANDS = ["Today's Forecast",
            "Week Forecast",
            "Year Forecast",
            "Options"]

OPTIONS_WIDTH = 1
OPTIONS = [
    "Settings",
    "Subscribe",
    "About"
]

FORECAST_RECIPIENT_WIDTH = 1
FORECAST_RECIPIENTS = [
    "Your sign",
    "Other sign"
]

ZODIAC_SIGNS_WIDTH = 3
ZODIAC_SIGNS = [
    'Aries',
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn',
    'Aquarius',
    'Pisces'
]

with open('config.yaml') as f:
    settings = yaml.load(f, Loader=yaml.loader.SafeLoader)

mode = None

bot = telebot.TeleBot(settings['bot_api_key'])


# React to /start
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=COMMAND_WIDTH)
    markup.add(*COMMANDS)
    bot.send_message(message.chat.id, "Choose Mode", reply_markup=markup)


def show_options(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=OPTIONS_WIDTH)
    markup.add(*[telebot.types.InlineKeyboardButton(option, callback_data=option) for option in OPTIONS])
    bot.send_message(message.chat.id, "Choose Option", reply_markup=markup)


def select_sign(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=ZODIAC_SIGNS_WIDTH)
    markup.add(
        *[telebot.types.InlineKeyboardButton(recipient, callback_data=recipient) for recipient in ZODIAC_SIGNS])
    bot.send_message(call.message.chat.id, "Which sign do you want a forecast for?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in FORECAST_RECIPIENTS)
def show_forecast_or_select_recipient(call):
    match call.data:
        case "Your sign":
            bot.send_message(call.message.chat.id, f"Showing forecast for {mode} for your sign")
        case "Other sign":
            select_sign(call)


@bot.callback_query_handler(func=lambda call: call.data in ZODIAC_SIGNS)
def show_forecast_for_sign(call):
    bot.send_message(call.message.chat.id, f"Showing forecast for {call.data}")


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
