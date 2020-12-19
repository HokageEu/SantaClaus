
import telebot
from telebot import types # кнопки
from string import Template

bot = telebot.TeleBot('свой токен')

user_dict = {}

class User:
    def __init__(self, taste):
        self.taste = taste

        keys = ['taste']
                
        for key in keys:
            self.key = None

@bot.message_handler(commands=["start"])
def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Введите ФИО', reply_markup=markup)
        bot.register_next_step_handler(msg, process_taste_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')



def process_taste_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.taste = message.text

        bot.send_message(chat_id, getRegData(user, 'Принято', message.from_user.first_name), parse_mode="Markdown")

        bot.send_message('сюда название чата', getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")


    except Exception as e:
        bot.reply_to(message, 'ooops!!')



# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template('$title *$name* \n  ФИО: *$taste* ')

    return t.substitute({
        'title': title,
        'name': name,
        'taste': user.taste,

        

    })




if __name__ == '__main__':
    bot.polling(none_stop=True)