import telebot
import yaml
from settings import *

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

mode = None
prev_chosen_sign = None
user_sign = None

bot = telebot.TeleBot(config['bot_api_key'])


# React to /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=COMMAND_WIDTH)
    markup.add(*COMMANDS)
    bot.send_message(message.chat.id, "Choose Mode", reply_markup=markup)


def show_options(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=OPTIONS_WIDTH)
    markup.add(*[telebot.types.InlineKeyboardButton(option, callback_data=option) for option in OPTIONS])
    bot.send_message(message.chat.id, "Choose Option", reply_markup=markup)


def select_sign(call, msg):
    markup = telebot.types.InlineKeyboardMarkup(row_width=ZODIAC_SIGNS_WIDTH)
    markup.add(
        *[telebot.types.InlineKeyboardButton(recipient, callback_data=recipient) for recipient in ZODIAC_SIGNS])
    bot.send_message(call.message.chat.id, msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in FORECAST_RECIPIENTS)
def show_forecast_or_select_recipient(call):
    match call.data:
        case "Your sign":
            bot.send_message(call.message.chat.id, f"Showing forecast for {mode} for your sign")
        case "Other sign":
            select_sign(call, "Which sign do you want a forecast for?")


@bot.callback_query_handler(func=lambda call: call.data in ZODIAC_SIGNS)
def show_forecast_for_sign(call):
    global prev_chosen_sign
    bot.send_message(call.message.chat.id, f"Showing forecast for {call.data}")
    prev_chosen_sign = call.data


@bot.callback_query_handler(func=lambda call: call.data in SETTINGS)
def select_settings(call):
    match call.data:
        case "Set your Sign":
            bot.send_message(call.message.chat.id, f"Changing Sign")
        case _:
            bot.send_message(call.message.chat.id, f"Showing Setting {call.data}")


def show_settings(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=SETTINGS_WIDTH)
    markup.add(*[telebot.types.InlineKeyboardButton(setting, callback_data=setting) for setting in SETTINGS])
    bot.send_message(call.message.chat.id, "Choose Option", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in OPTIONS)
def show_forecast_for_sign(call):
    match call.data:
        case "Settings":
            show_settings(call)
        case _:
            bot.send_message(call.message.chat.id, f"Showing Option {call.data}")


def select_recipient(message, forecast_mode):
    global mode
    mode = forecast_mode
    markup = telebot.types.InlineKeyboardMarkup(row_width=FORECAST_RECIPIENT_WIDTH)
    if prev_chosen_sign is not None:
        markup.add(telebot.types.InlineKeyboardButton(prev_chosen_sign, callback_data=prev_chosen_sign))
    if user_sign is not None:
        markup.add(telebot.types.InlineKeyboardButton(f'Your sign - {user_sign}', callback_data=user_sign))
    markup.add(telebot.types.InlineKeyboardButton("Other sign", callback_data="Other sign"))
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
