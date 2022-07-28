import telebot
import yaml
from settings import *
from horoscope_forecast_scraper import AstroWorldScraper
from datetime import datetime
from Library import get_zodiac_sign_by_birth_date

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

mode = None
prev_chosen_sign = None
user_sign = None
user_date_of_birth: datetime = datetime(2017, 2, 3, 8, 0, 0)

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
        case "User date of birth":
            print('here')
            show_forecast(call)
        case "Your sign":
            bot.send_message(call.message.chat.id, f"Showing forecast for {mode} for your sign")
        case "Other sign":
            select_sign(call, "Which sign do you want a forecast for?")


@bot.callback_query_handler(func=lambda call: call.data in ZODIAC_SIGNS)
def show_forecast(call):
    global prev_chosen_sign
    print(f"Showing forecast for {call.data}")
    prev_chosen_sign = call.data
    scrp = AstroWorldScraper(user_date_of_birth)
    match mode:
        case "Month":
            forecast = scrp.monthly_forecast(8, 2022)
            print(forecast)
            for paragraph in forecast:
                bot.send_message(call.message.chat.id, paragraph)
        case _:
            bot.send_message(call.message.chat.id, "Invalid Mode")


@bot.callback_query_handler(func=lambda call: call.data in SETTINGS)
def select_settings(call):
    match call.data:
        case "Set your Sign":
            bot.send_message(call.message.chat.id, f"Changing Sign")
        case "Set your Birth Date":
            markup = telebot.types.ForceReply(selective=True)
            bot.send_message(call.message.chat.id, f"Set Birth Date, format: dd/mm/yyyy hh:MM",
                             reply_markup=markup)
        case _:
            bot.send_message(call.message.chat.id, f"Showing Setting {call.data}")


def show_settings(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=SETTINGS_WIDTH)
    markup.add(*[telebot.types.InlineKeyboardButton(setting, callback_data=setting) for setting in SETTINGS])
    bot.send_message(call.message.chat.id, "Choose Option", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in OPTIONS)
def select_option(call):
    match call.data:
        case "Settings":
            show_settings(call)
        case _:
            bot.send_message(call.message.chat.id, f"Showing Option {call.data}")


def select_recipient(message, forecast_mode):
    global mode
    mode = forecast_mode
    markup = telebot.types.InlineKeyboardMarkup(row_width=FORECAST_RECIPIENT_WIDTH)
    if user_date_of_birth is not None:
        markup.add(telebot.types.InlineKeyboardButton(f"Date of birth - {user_date_of_birth.strftime('%d-%m-%Y')}",
                                                      callback_data="User date of birth"))
    else:
        markup.add(telebot.types.InlineKeyboardButton("Set date of birth", callback_data="Set your Birth Date"))
    if prev_chosen_sign is not None:
        markup.add(telebot.types.InlineKeyboardButton(prev_chosen_sign, callback_data=prev_chosen_sign))
    if user_sign is not None:
        markup.add(telebot.types.InlineKeyboardButton(f'Your sign - {user_sign}', callback_data=user_sign))
    markup.add(telebot.types.InlineKeyboardButton("Other sign", callback_data="Other sign"))
    bot.send_message(message.chat.id, "Which sign do you want a forecast for?", reply_markup=markup)


@bot.message_handler(regexp=r'\d\d/\d\d/\d\d\d\d \d\d:\d\d')
def set_user_birth_date(message):
    global user_date_of_birth, user_sign
    user_date_of_birth = datetime.strptime(message.text, '%d/%m/%Y %H:%M')
    print(message.text, user_date_of_birth)
    bot.send_message(message.chat.id, 'Date of birth set successfully!')
    user_sign = get_zodiac_sign_by_birth_date(user_date_of_birth)
    bot.send_message(message.chat.id, f'Your sign: {user_sign}')
    handle_start(message)


@bot.message_handler()
def handle_messages(message):
    match message.text:
        case "Options":
            print("Showing Options")
            show_options(message)
        case "Today's Forecast":
            select_recipient(message, forecast_mode="Today")
        case "Tomorrow's Forecast":
            select_recipient(message, forecast_mode="Tomorrow")
        case "Month Forecast":
            select_recipient(message, forecast_mode="Month")
        case "Year Forecast":
            select_recipient(message, forecast_mode="Year")
    print(message.text, "selected")


bot.polling()
