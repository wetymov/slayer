import sqlite3
import telebot
from telebot import types
import random
import time
token = '2069945398:AAGAkgtu3Cr2R0UH28R2BoEUKYaeD4F8ZZA'
bot = telebot.TeleBot(token)
conn = sqlite3.connect('clicker.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT INTO people (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()


def createslayer(name_slayer: str, owner:int, breath: str):
    cursor.execute('INSERT INTO slayer (name_slayer, owner, breath) VALUES (?, ?, ?)', (name_slayer, owner, breath))
    conn.commit()
    
@bot.message_handler(commands=['start'])#/start - обучение
def start_message(message):
    us_id = message.from_user.id
    r = cursor.execute(f'''SELECT slayer_id FROM slayer WHERE owner = {us_id}''').fetchone()
    if not(r is None):
        bot.send_message(message.chat.id, 'Чтобы управлять своим истребителем демонов /slayer')
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать')
        bot.send_message(message.chat.id, 'Чтобы создать или управлять своим истребителем демонов /slayer')
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)


@bot.message_handler(commands=['slayer'])
def slayer(message):
    us_id = message.from_user.id
    r = cursor.execute(f'''SELECT slayer_id FROM slayer WHERE owner = {us_id}''').fetchone()
    if not(r is None):
        name = cursor.execute(f'''SELECT name_slayer FROM slayer WHERE owner = {us_id}''').fetchone()
        hp = cursor.execute(f'''SELECT hp_slayer FROM slayer WHERE owner = {us_id}''').fetchone()
        power = cursor.execute(f'''SELECT power FROM slayer WHERE owner = {us_id}''').fetchone()
        bal = cursor.execute(f'''SELECT balance FROM slayer WHERE owner = {us_id}''').fetchone()
        lvl = cursor.execute(f'''SELECT level FROM slayer WHERE owner = {us_id}''').fetchone()
        dyh = cursor.execute(f'''SELECT breath FROM slayer WHERE owner = {us_id}''').fetchone()
        expi = cursor.execute(f'''SELECT exp FROM slayer WHERE owner = {us_id}''').fetchone()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Идти на миссию⚡️")
        markup.add(item1)
        item2 = types.KeyboardButton("Тренировка💪🏾")
        markup.add(item2)
        expMAX = int(lvl[0]) * 100
        if expi[0] >= expMAX:
            cursor.execute(f'''UPDATE slayer SET level == {lvl[0]+1} WHERE owner == {us_id}''')
            conn.commit()
            cursor.execute(f'''UPDATE slayer SET exp == {expMAX-expi[0]} WHERE owner == {us_id}''')
            conn.commit()
            expMAX += 100
        lvl = cursor.execute(f'''SELECT level FROM slayer WHERE owner = {us_id}''').fetchone()
        expi = cursor.execute(f'''SELECT exp FROM slayer WHERE owner = {us_id}''').fetchone()
        bot.send_message(message.chat.id, f'Имя - {name[0]}\nУровень - {lvl[0]}\nЗдоровье - {hp[0]} ❤️\nСила - {power[0]} ⚡️\nДыхание - {dyh[0]}\nБаланс - {bal[0]} монет\nОпыт - {expi[0]}/{expMAX} exp', reply_markup=markup)


    else:
        bot.send_message(message.chat.id, 'Создайте своего истребителя')
        msg = bot.send_message(message.chat.id, 'Введите имя своего истребителя')
        bot.register_next_step_handler(msg, nameslayer)


def nameslayer(message):
    global namesl
    namesl = message.text
    bot.send_message(message.chat.id, '1 - дыхание пламени\n2 - дыхание воды\n3 - дыхание звука\n4 - дыхание грома\n5 - дыхание любви\n6 - дыхание ветра\n7 - дыхание луны')
    msg = bot.send_message(message.chat.id, 'Введите номер дыхания: ')
    bot.register_next_step_handler(msg, breath)


def breath(message):
    if message.text.isdigit():
        brea = int(message.text)
        us_id = message.from_user.id
        if brea == 1:
            createslayer(name_slayer = namesl, owner = us_id, breath = 'Огонь')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        elif brea == 2:
            createslayer(name_slayer = namesl, owner = us_id,breath = 'Вода')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        elif brea == 3:
            createslayer(name_slayer = namesl,owner = us_id, breath = 'Звук')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        elif brea == 4:
            createslayer(name_slayer = namesl, owner = us_id,breath = 'Гром')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        elif brea == 5:
            createslayer(name_slayer = namesl,owner = us_id, breath = 'Любовь')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        elif brea == 6:
            createslayer(name_slayer = namesl, owner = us_id,breath = 'Ветер')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        elif brea == 7:
            createslayer(name_slayer = namesl,owner = us_id, breath = 'Луна')
            bot.send_message(message.chat.id, 'Создание персонажа закончилось')
            bot.send_message(message.chat.id, 'Для того, чтобы посмотреть свою статистику напиши /slayer')
        
        else:
            msg = bot.send_message(message.chat.id, 'Вы ввели не правильно число, введите заново: ')
            bot.register_next_step_handler(msg, breath)
        
            
@bot.message_handler(content_types=['text'])
def do(message):
    us_id = message.from_user.id
    r = cursor.execute(f'''SELECT slayer_id FROM slayer WHERE owner = {us_id}''').fetchone()
    if r is None:
        bot.send_message(message.chat.id, 'Эта фунция вам не допуступна\nСоздайте своего истребителя демонов /slayer')
    else:
        if 'идти на миссию' in message.text.lower():
            r = cursor.execute(f'''SELECT zan FROM slayer WHERE owner = {us_id}''').fetchone()
            if r[0] == 0:
                bot.send_message(message.chat.id, 'Ворон прислал вам задание: \n-Где-то поблизости есть демон, отправляйся на его убийство')
                bot.send_message(message.chat.id, 'Ваш персонаж вернется с миссии через 15 секунд')
                cursor.execute(f'''UPDATE slayer SET zan == 1 WHERE owner == {us_id}''')
                conn.commit()
                time.sleep(15)
                bal = cursor.execute(f'''SELECT balance FROM slayer WHERE owner = {us_id}''').fetchone()
                koif = cursor.execute(f'''SELECT koif FROM slayer WHERE owner = {us_id}''').fetchone()
                valera = int(bal[0]) + (100*koif[0])
                cursor.execute(f'''UPDATE slayer SET balance == {valera} WHERE owner == {us_id}''')
                conn.commit()
                nex = cursor.execute(f'''SELECT exp FROM slayer WHERE owner = {us_id}''').fetchone()
                nexon = 20 + int(nex[0])
                cursor.execute(f'''UPDATE slayer SET exp == {nexon} WHERE owner == {us_id}''')
                conn.commit()
                cursor.execute(f'''UPDATE slayer SET zan == 0 WHERE owner == {us_id}''')
                conn.commit()
                bot.send_message(message.chat.id, f'Персонаж вернулся с миссии и заработал 100 монет, ваш баланс равен {valera} монет')

            else:
                bot.send_message(message.chat.id, 'Персонаж занят')
                bot.send_message(message.chat.id, 'Подождите')
        elif 'магазин' in message.text.lower():
            print(0)
        elif 'тренировка' in message.text.lower():
            r = cursor.execute(f'''SELECT zan FROM slayer WHERE owner = {us_id}''').fetchone()
            if r[0] == 0:
                bot.send_message(message.chat.id, 'Вы начали тренировку')
                bot.send_message(message.chat.id, 'Время тренировки 20 секунд')
                cursor.execute(f'''UPDATE slayer SET zan == 1 WHERE owner == {us_id}''')
                conn.commit()
                time.sleep(20)
                cursor.execute(f'''UPDATE slayer SET zan == 0 WHERE owner == {us_id}''')
                conn.commit()
                nex = cursor.execute(f'''SELECT exp FROM slayer WHERE owner = {us_id}''').fetchone()
                nexon = 50 + int(nex[0])
                cursor.execute(f'''UPDATE slayer SET exp == {nexon} WHERE owner == {us_id}''')
                conn.commit()
                bot.send_message(message.chat.id, 'Ура!Тернировка подошла к концу\nВы заработали 50 опыта')



bot.polling(none_stop=0)
