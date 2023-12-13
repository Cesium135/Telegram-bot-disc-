from telebot import types
import telebot
bot = telebot.TeleBot('5697473675:AAFhssbvvkm4Kx2B5OoSo9W8qAyW3Llhj24')
import pandas as pd
import numpy as np

#settings 
autoansw={}  
name=''
text=''  
autoanswersettings=[]
token=''
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":    
        bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")   
    if message.text=='/menu':
        keyboard = types.InlineKeyboardMarkup(); 
        key_acc = types.InlineKeyboardButton(text='Аккаунты', callback_data='accs')
        key_help=types.InlineKeyboardButton(text='Помощь', callback_data='help')
        keyboard.add(key_acc,key_help)
        bot.send_message(message.chat.id, "тут будет меню",reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")
        
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global autoanswersettings
    accdata=pd.read_csv('accdata.csv', encoding='latin-1',sep=',')
    accs=accdata[accdata['TelegramId']==call.message.chat.id]
    if call.data == "accs":
        key_myacc = types.InlineKeyboardButton(text='Мои аккаунты', callback_data='myaccs')
        key_addacc=types.InlineKeyboardButton(text='Добавить аккаунт', callback_data='addacc')
        keyboard = types.InlineKeyboardMarkup(); 
        keyboard.add(key_myacc,key_addacc)
        bot.send_message(call.message.chat.id, "Меню аккаунтов",reply_markup=keyboard)
    elif call.data=='myaccs':
        keyboard = types.InlineKeyboardMarkup(); 
        for i in accs['Token'].values:
            cd=i
            key_acc=types.InlineKeyboardButton(text=i, callback_data=cd)
            keyboard.add(key_acc)
        bot.send_message(call.message.chat.id, "Ваши аккаунты",reply_markup=keyboard)
    elif call.data =="addacc":
        bot.send_message(call.message.chat.id, "Пожалуйста, введите токен")
        bot.register_next_step_handler(call.message,addnewacc)
    elif call.data =="autoanswer":
        accdata=pd.read_csv('answers.csv',index_col='ID', encoding='latin-1',sep=';')
        answers=accdata[accdata['Token']==token]
        key_anycity = types.InlineKeyboardButton(text='Добавить автоответ', callback_data='autoansweradd')
        keyboard = types.InlineKeyboardMarkup(); 
        keyboard.add(key_anycity)
        if len (answers)==0:
            bot.send_message(call.message.chat.id, "Автоответов нет",reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, "Автоответы",reply_markup=keyboard)
    elif call.data =='autoansweradd':
        autoanswersettings.append(token)
        autoanswersettings.append(call.message.chat.id)
        key_1stansw = types.InlineKeyboardButton(text='На 1ое сообщение', callback_data='1answ')
        key_trigger=types.InlineKeyboardButton(text='На триггер', callback_data='trigger')
        key_reviews = types.InlineKeyboardButton(text='На отзывы', callback_data='reviews')
        keyboard = types.InlineKeyboardMarkup(); 
        keyboard.add(key_1stansw,key_trigger,key_reviews)
        bot.send_message(call.message.chat.id, "Выберите тип автоответа",reply_markup=keyboard)
    elif call.data=='1answ':
        autoanswersettings.append('1stansw')
        autoanswersettings.append(None)
        
        bot.send_message(call.message.chat.id, "Настроено! Введите задержку")
        bot.register_next_step_handler(call.message,adddelay)
    elif call.data=='trigger':
            autoanswersettings.append('trigger')
            bot.register_next_step_handler(call.message,addtriggers)
        
    elif call.data=='reviews':
            autoanswersettings.append('reviews')
            autoanswersettings.append(None)
            key_anycity = types.InlineKeyboardButton(text='Добавить автоответ', callback_data='autoanswadd')
            keyboard = types.InlineKeyboardMarkup(); 
            keyboard.add(key_anycity)
    elif call.data in accs['Token'].values:
        key_auto=types.InlineKeyboardButton(text='Автоответы', callback_data='autoanswer')
        key_patt=types.InlineKeyboardButton(text='Шаблоны', callback_data='pattern')
        keyboard = types.InlineKeyboardMarkup(); 
        keyboard.add(key_auto, key_patt)
        bot.send_message(call.message.chat.id, "Ваш аккаунт:"+str(call.data),reply_markup=keyboard)

def help(message):
    pass

def addnewacc(message):
    global token
    token=message.text
    accdata=pd.read_csv('accdata.csv',index_col='Token', encoding='latin-1',sep=',')
    accdata.loc[token]=message.chat.id
    accdata.to_csv('accdata.csv')
    keyboard = types.InlineKeyboardMarkup(); 
    key_acc = types.InlineKeyboardButton(text='Аккаунты', callback_data='myaccs')
    key_auto=types.InlineKeyboardButton(text='Настроить автоответ этому аккаунту', callback_data='autoanswer')
    keyboard.add(key_acc,key_auto)
    bot.send_message(message.chat.id,'Аккаунт добавлен',reply_markup=keyboard)

def adddelay(message):
    global autoanswersettings
    autoanswersettings.append(message.text)
    accdata=pd.read_csv('autoanswerdata.csv', encoding='latin-1',sep=',')
    accdata[len(accdata['Token'])]=pd.Series(autoanswersettings)
    accdata.to_csv('autoanswerdata.csv')
    bot.send_message(message.chat.id, "Настроено! Введите название автоответа")
    bot.register_next_step_handler(message,autoanswerpatternname)
def autoanswerpatternname(message):
    global name
    name=message.text
    bot.send_message(message.chat.id, "Введите текст автоответа")
    bot.register_next_step_handler(message,autoanswerpattern)
def autoanswerpattern(message):
    global text, autoansw
    text=message.text
    
    key_myacc = types.InlineKeyboardButton(text='Мои аккаунты', callback_data='myaccs')
    keyboard = types.InlineKeyboardMarkup(); 
    keyboard.add(key_myacc)
    autoansw[name]=text
    answers=pd.read_csv('answers.csv',index_col='ID', encoding='latin-1',sep=';')
    serie=pd.Series(data=[autoanswersettings[0],name,text])
    print(answers)
    answers[len(answers['Token'])]=serie
    answers.to_csv('autoanswer')
    bot.send_message(message.chat.id, "Успешно добавлено!",reply_markup=keyboard)

def addtriggers(message):
    global autoanswersettings
    autoanswersettings.append(message.text.split('\n'))
    key_anycity = types.InlineKeyboardButton(text='Добавить автоответ', callback_data='autoanswadd')
    keyboard = types.InlineKeyboardMarkup(); 
    keyboard.add(key_anycity)
    



                
        
        
bot.polling(none_stop=True, interval=0)

