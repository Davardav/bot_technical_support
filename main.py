import telebot
from confing import * 
from logic import DB
from telebot import types
bot = telebot.TeleBot(TOKEN)

ans = {}
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"""Здравствуйте! Я бот Техподдержки.
Просмотрите быстрые вопросы 
Если вы не найдёте ответ вопрос,то вызовете специалиста 
Дополнительная информация по команде /help
""")
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, f"""Дополнительная информация по командам:
                 /start - стартовое сообщение
                 /help - справка по командам
                 /q - быстрые вопросы
                 /specialist - вызов специалиста
                 """)
    workers = manager.workers()
    for worker in workers:
        if int(worker) == int(message.chat.id):
            bot.reply_to(message, """Для работников:
                        /ans_to_q - получиить вопросы
                        После выбора вопроса напишите ответ
                         Не забудте быть вежливым
                         """)
    
@bot.message_handler(commands=['q'])
def button_message(message):
    markup = types.ReplyKeyboardRemove()
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    questions = manager.get_fast_q()
    for question in questions:
        item = types.KeyboardButton(question)
        markup.add(item)
    markup.add('нет в списке/написать специалисту')
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(commands=['ans_to_q'])
def user_q_a(message):
    markup = types.ReplyKeyboardRemove()
    workers = manager.workers()
    for worker in workers:
        if int(message.chat.id) == int(worker):
            q = manager.get_q()
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in q:
                w = manager.get_q_id(i)
                bot.send_message(message.chat.id,f"{i} - {w}")
                item = types.KeyboardButton(i)
                markup.add(item)
            bot.send_message(message.chat.id,'Выберите вопрос',reply_markup=markup)
            if len(q) == 0:
                bot.send_message(message.chat.id,'Список вопросов пуст')
    
@bot.message_handler(content_types='text')
def message_reply(message):
    questions = manager.get_fast_q()
    answers = manager.get_fast_a()
    if message.text=='нет в списке/написать специалисту' or message.text=='/specialist':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,'Опишите проблему проблему',reply_markup=markup)
        bot.register_next_step_handler(message, message_someone)
    
    for question in questions:
        if message.text==question:
            markup = types.ReplyKeyboardRemove()
            index = questions.index(question)
            bot.send_message(message.chat.id,answers[index], reply_markup=markup)
    workers = manager.workers()
    for worker in workers:
        if int(message.chat.id) == int(worker):
            q = manager.get_q()
            for i in q:
                if message.text== i :
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id,'Решити проблему', reply_markup=markup)
                    ans[message.chat.id] = i
                    bot.register_next_step_handler(message, an_q)
    
def message_someone(message):
    user = message.chat.id
    manager.add_q(message.text,user)
    bot.send_message(message.chat.id,'спасибо за вопрос, ожидайте ответа')
def an_q(message):
    q = ans.get(message.chat.id)
    id = manager.get_q_id(q)
    manager.n_ans(id,message.text)
    bot.send_message(message.chat.id,'спасибо за ответ')
    del ans[message.chat.id]
    user_name = manager.get_name_id(id)
    bot.send_message(user_name,f"""Вы получили ответ:
                    {message.text}""")
if __name__=="__main__":
    manager = DB(DATABASE)
    bot.polling()
