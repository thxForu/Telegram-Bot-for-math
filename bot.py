# -*- coding: utf-8 -*-
import telebot
from telebot import types
import os
from dotenv import load_dotenv
import traceback
import pymongo
import pprint
from bson.objectid import ObjectId
import time
load_dotenv()

bot = telebot.TeleBot('1870782408:AAFgZcSZCPTS_X9O0ckjUWbjr2FfhFjQTp4')


class Offer:
    def __init__(self, comp_name):
        self.comp_name = comp_name
        self.salary = None
        self.company_name = None
        self.description = None
        self.contact_info = None


class Summary:
    def __init__(self, name):
        self.name = name
        self.course = None
        self.first_name_last_name = None
        self.contact_info = None


Offer_dict = {}
summary_dict = {}
student_const = 'Студент'
employer_const = 'Роботодавець'
privateChatId = os.getenv('PRIVATE_CHAT_ID')
channelForSummary = os.getenv('CHANNEL_FOR_SUMMARY')
channelForOffer = os.getenv('CHANNEL_FOR_OFFER')
linkToChannelForSummary = os.getenv('LINK_TO_CHANNEL_FOR_SUMMARY')
linkToChannelForOffer = os.getenv('LINK_TO_CHANNEL_FOR_OFFER')
fac_and_spec = {'Біологічний факультет': ['Біологія', 'Садівництво та виноградарство', 'Середня освіта. Біологія та здоров’я людини'],
'Географічний факультет': ['Географія', 'Геодезія та землеустрій', 'Лісове господарство', 'Середня освіта. Географія'],
'Економічний факультет': ['Економіка', 'Облік і оподаткування', 'Підприємництво, торгівля та біржова діяльність', 'Фінанси, банківська справа та страхування'],
'Інженерно-технічний факультет': ['Автоматизація та комп’ютерно-інтегровані технології', 'Будівництво та цивільна інженерія', 'Електроніка Комп’ютерна інженерія', 'Прикладна механіка'],
'Медичний факультет': ['Медицина', 'Медсестринство. Екстрена медицина', 'Медсестринство. Медсестринство', 'Фармація, промислова фармація'],
'Стоматологічний факультет': ['Стоматологія'],
'Факультет здоров’я та фізичного виховання':['Психологія', 'Середня освіта. Фізична культура', 'Спеціальна освіта. Олігофренопедагогіка', 'Фізична культура і спорт', 'Фізична терапія, ерготерапія'],
'Факультет іноземної філології': ['Середня освіта. Англійська мова і література', 'Середня освіта. Німецька мова і література', 'Середня освіта. Румунська мова і література', 'Середня освіта. Французька мова і література Філологія.', 'Германські мови та літератури, перша – англійська',
'Філологія. Германські мови та літератури, перша – німецька', 'Філологія. Романські мови та літератури, перша – французька'],
'Факультет інформаційних технологій': ['Інженерія програмного забезпечення', 'Інформаційні системи та технології', 'Комп’ютерні науки'],
'Факультет історії та міжнародних відносин': ['Історія та археологія', 'Культурологія', 'Маркетинг', 'Менеджмент', 'Міжнародні відносини, суспільні комунікації та регіональні студії', 'Середня освіта. Історія' ],
'Факультет математики та цифрових технологій': ['Математика', 'Прикладна математика', 'Середня освіта. Математика', 'Системний аналіз'],
'Факультет міжнародних економічних відносин': ['Міжнародні економічні відносини', 'Філологія. Прикладна лінгвістика'],
'Факультет суспільних наук': ['Дошкільна освіта', 'Політологія', 'Початкова освіта', 'Психологія', 'Публічне управління та адміністрування', 'Соціальна робота', 'Соціологія', 'Філософія'],
'Факультет туризму та міжнародних комунікацій': ['Готельно-ресторанна справа', 'Туризм'],
'Фізичний факультет': ['Біомедична інженерія', 'Кібербезпека', 'Мікро- та наносистемна техніка', 'Прикладна фізика та наноматеріали', 'Середня освіта. Фізика', 'Телекомунікації та радіотехніка', 'Фізика та астрономія'],
'Філологічний факультет': ['Журналістика', 'Середня освіта. Російська мова і література', 'Середня освіта. Українська мова і література', 'Середня освіта. Українська мова і література', 'Філологія. Слов’янські мови та літератури, перша – російська', 'Філологія. Слов’янські мови та літератури, перша –словацька', 'Філологія. Слов’янські мови та літератури, перша –чеська', 'Філологія. Українська мова і література'],
'Хімічний факультет': ['Екологія', 'Середня освіта. Хімія', 'Хімічні технології та інженерія', 'Хімія'],
'Юридичний факультет': ['Міжнародне право', 'Право', 'Правоохоронна діяльність'],
'Українсько-угорський навчально-науковий інститут': ['Міжнародні відносини, суспільні комунікації та регіональні студії', 'Середня освіта. Історія', 'Середня освіта. Математика', 'Середня освіта. Угорська мова і література', 'Середня освіта. Фізика', 'Філологія. Угро-фінські мови та літератури, перша – угорська'],
'Природничо-гуманітарний фаховий коледж': ['Будівництво та цивільна інженерія', 'Геодезія та землеустрій', 'Інженерія програмного забезпечення', 'Облік і оподаткування', 'Право', 'Туризм', 'Фінанси, банківська справа та страхування']
}
direction_and_spec = {'Середня освіта': ['Середня освіта. Біологія та здоров’я людини', 'Середня освіта. Географія', 'Середня освіта. Фізика', 'Середня освіта. Математика'],
'Програмування ': ['Комп’ютерна інженерія', 'Системний аналіз'],
'Медицина': ['Медицина', 'Медсестринство. Екстрена медицина', 'Медсестринство. Медсестринство', 'Фармація, промислова фармація']
}

client = pymongo.MongoClient(
    os.getenv('MONGO_DB_TOKEN'))

db_name = os.getenv('MONGO_DB_NAME')
collection_offer = client[str(db_name)]['Offer']
collection_summary = client[str(db_name)]['Summary']
collection_verification = client[str(db_name)]['Verification']


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    try:
        start_keyboard = types.InlineKeyboardMarkup()
        summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                     url=linkToChannelForSummary)
        offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                   url=linkToChannelForOffer)
        start_keyboard.add(summary_channel, offer_channel)
        keyboard = types.InlineKeyboardMarkup()
        student_choice = types.InlineKeyboardButton(
            text="Студент", callback_data='student_choice')
        employer_choice = types.InlineKeyboardButton(
            text="Роботодавець", callback_data='employer_choice')

        print('USER ID:'+str(message.from_user.id))

        keyboard.add(student_choice, employer_choice)

        bot.reply_to(message, 'Вас вітає Бот для пошуку вакансій та розміщення резюме!',
                     reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        print(e.with_traceback)


def process_who_am_i(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        student_choice = types.InlineKeyboardButton(
            text="Студент", callback_data='student_choice')
        employer_choice = types.InlineKeyboardButton(
            text="Роботодавець", callback_data='employer_choice')

        keyboard.add(student_choice, employer_choice)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Ви студент чи роботодавець', reply_markup=keyboard)

        if message.text == student_const:
            msg = bot.reply_to(
                message, 'Введіть мови програмування які ви знаєте(через пробіл):')
            bot.register_next_step_handler(msg, name_step)
            return

        elif message.text == employer_const:
            msg = bot.reply_to(message, 'Введіть будь ласка посаду:')
            bot.register_next_step_handler(msg, company_name)
            return

        else:
            msg = bot.reply_to(message, 'Ви вибрали не конектну відповідь.')
            bot.register_next_step_handler(msg, process_who_am_i)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


'''
#Employer Section
'''

def company_name(message):
    try:
        chat_id = message.chat.id
        print('Chat id: '+str(chat_id))
        print('User id in pos stet'+str(message.from_user.id))
        comp_name = message.text
        offer = Offer(comp_name)
        Offer_dict[chat_id] = offer
        msg = bot.send_message(chat_id, text='Вакансія:')
        bot.register_next_step_handler(msg, vacantion)


    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')

def vacantion(message):
    try:
        chat_id = message.chat.id
        offer = Offer_dict[chat_id]
        vacantion = message.text
        offer.vacantion = vacantion
        markup = types.InlineKeyboardMarkup(row_width=1)
        high_school_yes = types.InlineKeyboardButton(text='Так', callback_data='high_school' + ',' + 'Так')
        high_school_no = types.InlineKeyboardButton(text='Ні', callback_data='high_school' + ',' + 'Ні')
        markup.add(high_school_yes, high_school_no)
        bot.send_message(chat_id, text='Вимоги до кандидатів:\nЗакінчена вища освіта:', reply_markup=markup)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def othe_progress(message):
    try:
        chat_id = message.chat.id
        other = message.text
        print(other)
        offer = Offer_dict[chat_id]
        offer.other = other
        markup = types.InlineKeyboardMarkup(row_width=1)
        official_work_yes = types.InlineKeyboardButton(text='Так', callback_data='official_work' + ',' + 'Так')
        official_work_no = types.InlineKeyboardButton(text='Ні', callback_data='official_work' + ',' + 'Ні')
        markup.add(official_work_yes, official_work_no)
        bot.send_message(chat_id, text='Вимоги до кандидатів:\nЗакінчена вища освіта:', reply_markup=markup)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def process_salary(message):
    try:
        chat_id = message.chat.id
        offer = Offer_dict[chat_id]
        salary = message.text
        markup = types.ReplyKeyboardMarkup()
        if not salary.isdigit() and salary != 'Договірна':
            msg = bot.send_message(chat_id, 'Заробітна плата повинна бути числом')
            bot.register_next_step_handler(msg, process_salary)
            return
        if salary == 0:
            offer.salary = 'Договірна'
        offer.salary = salary
        msg = bot.send_message(chat_id, 'Більш детальний опис вакансії:')
        bot.register_next_step_handler(msg, description_progress)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def description_progress(message):
    try:
        chat_id = message.chat.id
        description = message.text
        print(description)
        offer = Offer_dict[chat_id]
        offer.description = description
        msg = bot.send_message(chat_id, text='За детальною інформацією звертатися:')
        bot.register_next_step_handler(msg, offer_contact_info)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def offer_contact_info(message):
    try:
        chat_id = message.chat.id
        contact_info = message.text
        offer = Offer_dict[chat_id]
        offer.contact_info = contact_info
        markup = types.InlineKeyboardMarkup()
        personal_consent = types.InlineKeyboardButton(text="✅ Даю згоду", callback_data='offer_verefication' + ',' + str(chat_id))
        markup.add(personal_consent)
        bot.send_message(chat_id, 'Згода на використання персональних даних', reply_markup=markup)

    except Exception as e:
        print(e)
        bot.reply_to(
            message, 'Помилка зчитування контактної інформації чи що там...')


'''
# Student Section
'''


def name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        summary = Summary(name)
        summary_dict[chat_id] = summary
        summary.name = name
        msg = bot.send_message(
            chat_id, 'Вік:')
        bot.register_next_step_handler(msg, age_step)
    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка в зчитуванні курса...')


def age_step(message):
    try:
        chat_id = message.chat.id
        age = int(message.text)
        summary = summary_dict[chat_id]
        summary.age = str(age)
        faculty = fac_and_spec
        keyboard = types.InlineKeyboardMarkup()
        bruch = list(faculty.keys())
        for key in bruch:
            keyboard.add(types.InlineKeyboardButton(text=str(key), callback_data='fac_st,' + str(key[0:29])))
        bot.send_message(chat_id, text='Факультет', reply_markup=keyboard)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка')


def process_course_step(message):
    try:
        chat_id = message.chat.id
        course = int(message.text)
        if course > 0 and course < 7:
            summary = summary_dict[chat_id]
            summary.course = str(course)
            markup = types.InlineKeyboardMarkup(row_width=1)
            yes = types.InlineKeyboardButton(text='Високий рівень', callback_data='english_know'+','+'Високий рівень')
            midl = types.InlineKeyboardButton(text='Середній рівень', callback_data='english_know' + ',' + 'Середній рівень')
            no = types.InlineKeyboardButton(text='Не володію',
                                            callback_data='english_know' + ',' + 'Не володію')
            markup.add(yes, midl, no)
            bot.send_message(chat_id, 'Знання англійської мови', reply_markup=markup)

        else:
            msg = bot.reply_to(message, 'Введіть курс коректтно.')
            bot.register_next_step_handler(msg, process_course_step)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка в зчитувані курса...')


def personal_qualities(message):
    try:
        chat_id = message.chat.id
        personal_qualities = message.text
        print(personal_qualities)
        summary = summary_dict[chat_id]
        summary.personal_qualities = personal_qualities
        msg = bot.send_message(chat_id, 'Інші навички:')
        bot.register_next_step_handler(msg, another)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка')


def another(message):
    try:
        chat_id = message.chat.id
        another = message.text
        summary = summary_dict[chat_id]
        summary.another = another
        print(another)
        msg = bot.send_message(chat_id, 'Досвід роботи:')
        bot.register_next_step_handler(msg, experience)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'Помилка')


def experience(message):
    try:
        chat_id = message.chat.id
        experience = message.text
        print(experience)
        summary = summary_dict[chat_id]
        summary.experience = experience
        msg = bot.send_message(chat_id, 'Контактний телефон:')
        bot.register_next_step_handler(msg, summary_contact_info)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'Помилка')


def summary_contact_info(message):
    try:
        chat_id = message.chat.id
        contact_info = message.text
        print(contact_info)
        summary = summary_dict[chat_id]
        summary.contact_info = contact_info
        msg = bot.send_message(chat_id, 'Адреса електронної пошти:')
        bot.register_next_step_handler(msg, email_summary)


    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'Помилка')


def email_summary(message):
    try:
        chat_id = message.chat.id
        email_summary = message.text
        print(email_summary)
        summary = summary_dict[chat_id]
        summary.email = email_summary
        markup = types.InlineKeyboardMarkup()
        personal_consent = types.InlineKeyboardButton(text="✅ Даю згоду", callback_data='summary_verefication')
        markup.add(personal_consent)
        bot.send_message(chat_id, 'Згода на використання персональних даних', reply_markup=markup)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'Помилка')


# Функції для редагування вакансій
def position_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"position": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        position_change = types.InlineKeyboardButton(
            text="Посаду", callback_data='position_change,'+str(obj))
        salary_change = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,'+str(obj))
        name_change = types.InlineKeyboardButton(
            text="Назву компанії", callback_data='name_change,'+str(obj))
        description_change = types.InlineKeyboardButton(
            text="Опис компанії", callback_data='description_change,'+str(obj))
        contact_info_change = types.InlineKeyboardButton(
            text="Контактні дані", callback_data='contact_info_change,'+str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,'+str(obj))
        keyboard.add(position_change, salary_change, name_change, description_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💼 ' + change_1['position']
                                    + '\n💵 ' + change_1['salary']
                                    + '\n🏢 ' + change_1['company_name']
                                    + '\n📋 ' + change_1['description']
                                    + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)



    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def salary_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"salary": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        position_change = types.InlineKeyboardButton(
            text="Посаду", callback_data='position_change,'+str(obj))
        salary_change = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,'+str(obj))
        name_change = types.InlineKeyboardButton(
            text="Назву компанії", callback_data='name_change,'+str(obj))
        description_change = types.InlineKeyboardButton(
            text="Опис компанії", callback_data='description_change,'+str(obj))
        contact_info_change = types.InlineKeyboardButton(
            text="Контактні дані", callback_data='contact_info_change,'+str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,'+str(obj))
        keyboard.add(position_change, salary_change, name_change, description_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💼 ' + change_1['position']
                                    + '\n💵 ' + change_1['salary']
                                    + '\n🏢 ' + change_1['company_name']
                                    + '\n📋 ' + change_1['description']
                                    + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)



    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def name_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"company_name": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        position_change = types.InlineKeyboardButton(
            text="Посаду", callback_data='position_change,'+str(obj))
        salary_change = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,'+str(obj))
        name_change = types.InlineKeyboardButton(
            text="Назву компанії", callback_data='name_change,'+str(obj))
        description_change = types.InlineKeyboardButton(
            text="Опис компанії", callback_data='description_change,'+str(obj))
        contact_info_change = types.InlineKeyboardButton(
            text="Контактні дані", callback_data='contact_info_change,'+str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,'+str(obj))
        keyboard.add(position_change, salary_change, name_change, description_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💼 ' + change_1['position']
                                    + '\n💵 ' + change_1['salary']
                                    + '\n🏢 ' + change_1['company_name']
                                    + '\n📋 ' + change_1['description']
                                    + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def description_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"description": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        position_change = types.InlineKeyboardButton(
            text="Посаду", callback_data='position_change,'+str(obj))
        salary_change = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,'+str(obj))
        name_change = types.InlineKeyboardButton(
            text="Назву компанії", callback_data='name_change,'+str(obj))
        description_change = types.InlineKeyboardButton(
            text="Опис компанії", callback_data='description_change,'+str(obj))
        contact_info_change = types.InlineKeyboardButton(
            text="Контактні дані", callback_data='contact_info_change,'+str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,'+str(obj))
        keyboard.add(position_change, salary_change, name_change, description_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💼 ' + change_1['position']
                                    + '\n💵 ' + change_1['salary']
                                    + '\n🏢 ' + change_1['company_name']
                                    + '\n📋 ' + change_1['description']
                                    + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def contact_info_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"contact_info": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        position_change = types.InlineKeyboardButton(
            text="Посаду", callback_data='position_change,' + str(obj))
        salary_change = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,' + str(obj))
        name_change = types.InlineKeyboardButton(
            text="Назву компанії", callback_data='name_change,' + str(obj))
        description_change = types.InlineKeyboardButton(
            text="Опис компанії", callback_data='description_change,' + str(obj))
        contact_info_change = types.InlineKeyboardButton(
            text="Контактні дані", callback_data='contact_info_change,' + str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,' + str(obj))
        keyboard.add(position_change, salary_change, name_change, description_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💼 ' + change_1['position']
                                       + '\n💵 ' + change_1['salary']
                                       + '\n🏢 ' + change_1['company_name']
                                       + '\n📋 ' + change_1['description']
                                       + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')

# Функції для редагування резюме


def n_a_m_e_change(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"name": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        summary = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        name_change = types.InlineKeyboardButton(
            text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
        age_change = types.InlineKeyboardButton(
            text="Вік", callback_data='age_change,' + str(summary['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(summary['_id']))
        personal_qualities_change = types.InlineKeyboardButton(
            text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
        another = types.InlineKeyboardButton(
            text="Інші навички", callback_data='another_change,' + str(summary['_id']))
        experience = types.InlineKeyboardButton(
            text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
        end = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, end)
        bot.send_message(chat_id, text='Прізвище, ім’я, по батькові: ' + summary['name']
                                    + '\nВік: ' + summary['age']
                                    + '\nФакультет: ' + summary['faculty']
                                    + '\nСпеціальність: ' + summary['specialty']
                                    + '\nКурс: ' + summary['course']
                                    + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                                    + '\nОсобисті якості: ' + summary['personal_qualities']
                                    + '\nІнші навички: ' + summary['another']
                                    + '\nДосвід роботи: ' + summary['experience']
                                    + '\nКонтактний телефон: ' + summary['contact_info']
                                    + '\nАдреса електронної пошти: ' + summary['email'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def age_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"age": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        summary = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        name_change = types.InlineKeyboardButton(
            text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
        age_change = types.InlineKeyboardButton(
            text="Вік", callback_data='age_change,' + str(summary['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(summary['_id']))
        personal_qualities_change = types.InlineKeyboardButton(
            text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
        another = types.InlineKeyboardButton(
            text="Інші навички", callback_data='another_change,' + str(summary['_id']))
        experience = types.InlineKeyboardButton(
            text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
        end = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, end)
        bot.send_message(chat_id,  text='Прізвище, ім’я, по батькові: ' + summary['name']
                                    + '\nВік: ' + summary['age']
                                    + '\nФакультет: ' + summary['faculty']
                                    + '\nСпеціальність: ' + summary['specialty']
                                    + '\nКурс: ' + summary['course']
                                    + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                                    + '\nОсобисті якості: ' + summary['personal_qualities']
                                    + '\nІнші навички: ' + summary['another']
                                    + '\nДосвід роботи: ' + summary['experience']
                                    + '\nКонтактний телефон: ' + summary['contact_info']
                                    + '\nАдреса електронної пошти: ' + summary['email'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def course_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"course": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        summary = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        name_change = types.InlineKeyboardButton(
            text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
        age_change = types.InlineKeyboardButton(
            text="Вік", callback_data='age_change,' + str(summary['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(summary['_id']))
        personal_qualities_change = types.InlineKeyboardButton(
            text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
        another = types.InlineKeyboardButton(
            text="Інші навички", callback_data='another_change,' + str(summary['_id']))
        experience = types.InlineKeyboardButton(
            text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
        end = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, end)
        bot.send_message(chat_id, text='Прізвище, ім’я, по батькові: ' + summary['name']
                                    + '\nВік: ' + summary['age']
                                    + '\nФакультет: ' + summary['faculty']
                                    + '\nСпеціальність: ' + summary['specialty']
                                    + '\nКурс: ' + summary['course']
                                    + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                                    + '\nОсобисті якості: ' + summary['personal_qualities']
                                    + '\nІнші навички: ' + summary['another']
                                    + '\nДосвід роботи: ' + summary['experience']
                                    + '\nКонтактний телефон: ' + summary['contact_info']
                                    + '\nАдреса електронної пошти: ' + summary['email'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def pers_quali_change(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"personal_qualities": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        summary = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        name_change = types.InlineKeyboardButton(
            text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
        age_change = types.InlineKeyboardButton(
            text="Вік", callback_data='age_change,' + str(summary['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(summary['_id']))
        personal_qualities_change = types.InlineKeyboardButton(
            text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
        another = types.InlineKeyboardButton(
            text="Інші навички", callback_data='another_change,' + str(summary['_id']))
        experience = types.InlineKeyboardButton(
            text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
        end = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, end)
        bot.send_message(chat_id, text='Прізвище, ім’я, по батькові: ' + summary['name']
                                    + '\nВік: ' + summary['age']
                                    + '\nФакультет: ' + summary['faculty']
                                    + '\nСпеціальність: ' + summary['specialty']
                                    + '\nКурс: ' + summary['course']
                                    + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                                    + '\nОсобисті якості: ' + summary['personal_qualities']
                                    + '\nІнші навички: ' + summary['another']
                                    + '\nДосвід роботи: ' + summary['experience']
                                    + '\nКонтактний телефон: ' + summary['contact_info']
                                    + '\nАдреса електронної пошти: ' + summary['email'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def another_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"another": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        summary = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        name_change = types.InlineKeyboardButton(
            text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
        age_change = types.InlineKeyboardButton(
            text="Вік", callback_data='age_change,' + str(summary['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(summary['_id']))
        personal_qualities_change = types.InlineKeyboardButton(
            text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
        another = types.InlineKeyboardButton(
            text="Інші навички", callback_data='another_change,' + str(summary['_id']))
        experience = types.InlineKeyboardButton(
            text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
        end = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, end)
        bot.send_message(chat_id, text='Прізвище, ім’я, по батькові: ' + summary['name']
                                    + '\nВік: ' + summary['age']
                                    + '\nФакультет: ' + summary['faculty']
                                    + '\nСпеціальність: ' + summary['specialty']
                                    + '\nКурс: ' + summary['course']
                                    + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                                    + '\nОсобисті якості: ' + summary['personal_qualities']
                                    + '\nІнші навички: ' + summary['another']
                                    + '\nДосвід роботи: ' + summary['experience']
                                    + '\nКонтактний телефон: ' + summary['contact_info']
                                    + '\nАдреса електронної пошти: ' + summary['email'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')

def experience_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"experience": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        summary = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        name_change = types.InlineKeyboardButton(
            text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
        age_change = types.InlineKeyboardButton(
            text="Вік", callback_data='age_change,' + str(summary['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(summary['_id']))
        personal_qualities_change = types.InlineKeyboardButton(
            text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
        another = types.InlineKeyboardButton(
            text="Інші навички", callback_data='another_change,' + str(summary['_id']))
        experience = types.InlineKeyboardButton(
            text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
        end = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, end)
        bot.send_message(chat_id, text='Прізвище, ім’я, по батькові: ' + summary['name']
                                       + '\nВік: ' + summary['age']
                                       + '\nФакультет: ' + summary['faculty']
                                       + '\nСпеціальність: ' + summary['specialty']
                                       + '\nКурс: ' + summary['course']
                                       + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                                       + '\nОсобисті якості: ' + summary['personal_qualities']
                                       + '\nІнші навички: ' + summary['another']
                                       + '\nДосвід роботи: ' + summary['experience']
                                       + '\nКонтактний телефон: ' + summary['contact_info']
                                       + '\nАдреса електронної пошти: ' + summary['email'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


# Функція яка запускає видалення вакансій і резюме

@bot.message_handler(commands=['delete'])
def calling(message):
    try:
        keyboard_1 = types.InlineKeyboardMarkup()
        offer_cal = types.InlineKeyboardButton(
            text='Мої вакансії', callback_data='offer_cal')
        summary_cal = types.InlineKeyboardButton(
            text='Мої резюме', callback_data='summary_cal')
        keyboard_1.add(offer_cal, summary_cal)
        bot.send_message(message.chat.id, text='Оберіть, що бажаєте редагувати', reply_markup=keyboard_1)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


@bot.callback_query_handler(func=lambda call: True)
def send_to_channel(call):
    try:
        if call.data == 'test':
            print('call test data ')

        elif call.data == 'who_am_i':
            chat_id = call.message.chat.id
            keyboard = types.InlineKeyboardMarkup()
            student_choice = types.InlineKeyboardButton(
                text="Студент", callback_data='student_choice')
            employer_choice = types.InlineKeyboardButton(
                text="Роботодавець", callback_data='employer_choice')

            keyboard.add(student_choice, employer_choice)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ви студент чи роботодавець?', reply_markup=keyboard)
        elif call.data == 'change_view':
            chat_id = call.message.chat.id

        elif call.data == 'student_choice':
            chat_id = call.message.chat.id
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='new_summary')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')

            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ви зараз на стороні студента', reply_markup=reply_markup)

        elif call.data == 'employer_choice':
            chat_id = call.message.chat.id

            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі резюме", callback_data='get_list_summary')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            keyboard = [[choose, employer_button], [student_button]]

            reply_markup = types.InlineKeyboardMarkup(keyboard)
            msg = bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Ви зараз на стороні роботодавця:', reply_markup=reply_markup)

        elif call.data == 'new_summary':
            chat_id = call.message.chat.id
            msg = bot.send_message(
                chat_id=chat_id, text='Прізвище, ім’я, по батькові:')

            bot.register_next_step_handler(msg, name_step)

        elif call.data == 'new_offer':
            chat_id = call.message.chat.id
            msg = bot.send_message(
                chat_id=chat_id, text='Назва компанії/установи/організації:')
            bot.register_next_step_handler(msg, company_name)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif 'offer_verefication' in call.data:
            data = call.data.split(',')
            chat_id = call.message.chat.id
            user_id = data[1]
            offer = Offer_dict[chat_id]
            print('User id id verif button'+str(call.message.from_user.id))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='\nВаше резюме прийнято для обробки та перевірки. Очікуйте на повідомлення')
            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='offer_approve,'+str(chat_id)+','+str(user_id))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='offer_cancel,'+str(chat_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='offer_change,')
            keyboard.add(approve, cancel, change)
            message_save = bot.send_message(chat_id=privateChatId, text='Назва компанії/установи/організації: ' + offer.comp_name
                             + '\nВакансія: ' + offer.vacantion
                             + '\nЗакінчена вища освіта: ' + offer.high_school
                             + '\nСпеціальність: ' + offer.direction
                             + '\nЗнання англійської мови: ' + offer.english
                             + '\nІнші вимоги: ' + offer.other
                             + '\nОфіційне працевлаштування: ' + offer.official_work
                             + '\nМожливість працювати віддалено: ' + offer.remote_job
                             + '\nЗаробітна плата: ' + offer.salary
                             + '\nБільш детальний опис вакансії: ' + offer.description
                             + '\nЗа детальною інформацією звертатися: ' + offer.contact_info, reply_markup=keyboard)

            check_connections_with_db()
            offer_to_db = {
                'user_id': user_id,
                'company_name': offer.comp_name,
                'vacantion': offer.vacantion,
                'high_school': offer.high_school,
                'direction': offer.direction,
                'english': offer.english,
                'other': offer.other,
                'official_work': offer.official_work,
                'remote_job': offer.remote_job,
                'salary': offer.salary,
                'description': offer.description,
                'contact_info': offer.contact_info,
                'message_id': message_save.message_id
            }
            # Send offer to db
            collection_verification.insert_one(offer_to_db)

        elif 'offer_approve' in call.data:
            message_id = call.message.message_id
            offer = collection_verification.find_one({'message_id': message_id})
            obj = offer['_id']
            print(call.data)
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[2])
            link = bot.create_chat_invite_link(channelForSummary, member_limit=1)
            c = collection_offer.find_one({'user_id': str(user_id)})
            print(user_id, chat_id)
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі резюме", callback_data='get_list_summary')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')

            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Вашу вакансію опубліковано!' + str(link.invite_link), reply_markup=reply_markup)
            else:
                bot.send_message(
                    chat_id=chat_id, text='Вашу вакансію опубліковано!', reply_markup=reply_markup)

            message_offer_save = bot.send_message(chat_id=channelForOffer, text='💼 ' + offer['position']
                             + '\n💵 ' + offer['salary']
                             + '\n🏢 ' + offer['company_name']
                             + '\n📋 ' + offer['description']
                             + '\n📞 ' + offer['contact_info'])

            check_connections_with_db()
            offer_to_db = {
                'user_id': offer['user_id'],
                'position': offer['position'],
                'salary': offer['salary'],
                'company_name': offer['company_name'],
                'description': offer['description'],
                'contact_info': offer['contact_info'],
                'message_id': message_offer_save.message_id
            }
            # Send offer to db
            collection_offer.insert_one(offer_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})

        elif 'change_konec,' in call.data:  # закінчує редагування вакансії, копіює вакансію з колекції верифікації в колекцію оффера, постить в канал оффера і видпляє з колекції верифікації
            print(call.data)
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[1])
            obj = data[2]
            offer_vacantion = collection_verification.find_one({'_id':  ObjectId("{}".format(obj))})
            link = bot.create_chat_invite_link(channelForSummary, member_limit=1)
            c = collection_offer.find_one({'user_id': str(user_id)})
            print(user_id, chat_id)
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі резюме", callback_data='get_list_summary')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')

            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)

            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Вашу вакансію опубліковано!' + str(link.invite_link),
                    reply_markup=reply_markup)
            else:
                bot.send_message(
                    chat_id=chat_id, text='Вашу вакансію опубліковано!', reply_markup=reply_markup)
            message_offer_save = bot.send_message(chat_id=channelForOffer, text='💼 ' + offer_vacantion['position']
                                                                                + '\n💵 ' + offer_vacantion["salary"]
                                                                                + '\n🏢 ' + offer_vacantion["company_name"]
                                                                                + '\n📋 ' + offer_vacantion['description']
                                                                                + '\n📞 ' + offer_vacantion['contact_info'])

            check_connections_with_db()
            offer_to_db = {
                'user_id': offer_vacantion['user_id'],
                'position':  offer_vacantion['position'],
                'salary':  offer_vacantion['salary'],
                'company_name':  offer_vacantion['company_name'],
                'description':  offer_vacantion['description'],
                'contact_info':  offer_vacantion['contact_info'],
                'message_id': message_offer_save.message_id
            }
            # Send offer to db
            collection_offer.insert_one(offer_to_db)
            collection_verification.delete_one({'_id':  ObjectId("{}".format(obj))})

        elif 'offer_cancel' in call.data:
            data = call.data.split(',')
            chat_id = int(data[1])
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі резюме", callback_data='get_list_summary')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=chat_id, text='Вашу вакансію відхилeно!', reply_markup=reply_markup)

        elif 'offer_change' in call.data:  # запускає редагування вакансії
            chat = call.from_user.id
            message_id = call.message.message_id
            print(message_id)
            change = collection_verification.find_one({'message_id': message_id})
            keyboard = types.InlineKeyboardMarkup()
            position_change = types.InlineKeyboardButton(
                text="Посаду", callback_data='position_change,'+str(change['_id']))
            salary_change = types.InlineKeyboardButton(
                text="Заробітну плату", callback_data='salary_change,'+str(change['_id']))
            name_change = types.InlineKeyboardButton(
                text="Назву компанії", callback_data='name_change,'+str(change['_id']))
            description_change = types.InlineKeyboardButton(
                text="Опис компанії", callback_data='description_change,'+str(change['_id']))
            contact_info_change = types.InlineKeyboardButton(
                text="Контактні лані", callback_data='contact_info_change,'+str(change['_id']))
            keyboard.add(position_change, salary_change, name_change, description_change, contact_info_change)
            bot.send_message(chat, text='💼 ' + change['position']
                             + '\n💵 ' + change['salary']
                             + '\n🏢 ' + change['company_name']
                             + '\n📋 ' + change['description']
                             + '\n📞 ' + change['contact_info'])
            bot.send_message(chat, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

        elif 'position_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Введіть нову посаду:')
            bot.register_next_step_handler(msg, position_change_progress)

        elif 'salary_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Ведіть нову заробітну плату:')
            bot.register_next_step_handler(msg, salary_change_progress)

        elif 'name_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Ведіть нову назву копмпанії:')
            bot.register_next_step_handler(msg, name_change_progress)

        elif 'description_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text='Ведіть новий опис компанії:')
            bot.register_next_step_handler(msg, description_change_progress)

        elif 'contact_info_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text='Ведіть нові контактні дані:')
            bot.register_next_step_handler(msg, contact_info_change_progress)

        elif 'offer_ch_end' in call.data:  # це викликається кнопкою "закінчити редагування"
            data = call.data.split(',')
            id_object = data[1]
            offer_b = collection_verification.find_one({'_id':  ObjectId("{}".format(id_object))})
            user_id = offer_b['user_id']
            print('User id id verif button' + str(call.message.from_user.id))
            bot.delete_message(chat_id=privateChatId, message_id=offer_b['message_id'])
            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='change_konec,'+str(user_id)+','+str(id_object))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='offer_cancel,' + str(user_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='offer_change,')
            keyboard.add(approve, cancel, change)
            message_save = bot.send_message(privateChatId, text='💼 ' + offer_b['position']
                                                                        + '\n💵 ' + offer_b['salary']
                                                                        + '\n🏢 ' + offer_b['company_name']
                                                                        + '\n📋 ' + offer_b['description']
                                                                        + '\n📞 ' + offer_b['contact_info'],
                                            reply_markup=keyboard)
            collection_verification.update_one({"_id": ObjectId("{}".format(id_object))}, {'$set': {"message_id": message_save.message_id}})

        elif 'summary_verefication' in call.data:
            chat_id = call.message.chat.id
            summary = summary_dict[chat_id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='\nВаше резюме прийнято для обробки та перевірки. Очікуйте на повідомлення')

            print('UserId in sum veref: '+str(chat_id))

            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='summary_approve,'+str(chat_id)+','+str(chat_id))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='summary_cancel,'+str(chat_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='summary_change,')
            keyboard.add(approve, cancel, change)
            message_summary_save = bot.send_message(chat_id=privateChatId, text='Прізвище, ім’я, по батькові:' + summary.name
                             + '\nВік: ' + summary.age
                             + '\nФакультет: ' + summary.faculty
                             + '\nСпеціальність: ' + summary.specialty
                             + '\nКурс: ' + summary.course
                             + '\nЗнання англійської мови: ' + summary.english_know_lvl
                             + '\nОсобисті якості: ' + summary.personal_qualities
                             + '\nІнші навички: ' + summary.another
                             + '\nДосвід роботи: ' + summary.experience
                             + '\nКонтактний телефон: ' + summary.contact_info
                             + '\nАдреса електронної пошти: ' + summary.email, reply_markup=keyboard)

            check_connections_with_db()
            summary_to_db = {
                'user_id': chat_id,
                'name': summary.name,
                'age': summary.age,
                'faculty': summary.faculty,
                'specialty': summary.specialty,
                'course': summary.course,
                'english_know_lvl': summary.english_know_lvl,
                'personal_qualities': summary.personal_qualities,
                'another': summary.another,
                'experience': summary.experience,
                'contact_info': summary.contact_info,
                'email': summary.email,
                'message_id': message_summary_save.message_id
            }
            # Send summary to db
            collection_verification.insert_one(summary_to_db)

        elif 'summary_approve' in call.data:
            message_id = call.message.message_id
            summary = collection_verification.find_one({"message_id": message_id})
            obj = summary['_id']
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[2])
            link = bot.create_chat_invite_link(channelForOffer, member_limit=1)
            c = collection_summary.find_one({'user_id': int(user_id)})
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='student_choice')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме опубліковано!' + str(link.invite_link), reply_markup=reply_markup)
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме опубліковано!', reply_markup=reply_markup)

            message_save = bot.send_message(chat_id=channelForSummary, text='Прізвище, ім’я, по батькові:' + summary['name']
                             + '\nВік: ' + summary['age']
                             + '\nФакультет:' + summary['faculty']
                             + '\nСпеціальність:' + summary['specialty']
                             + '\nКурс:' + summary['course']
                             + '\nЗнання англійської мови:' + summary['english_know_lvl']
                             + '\nОсобисті якості:' + summary['personal_qualities']
                             + '\nІнші навички:' + summary['another']
                             + '\nДосвід роботи:' + summary['experience']
                             + '\nКонтактний телефон:' + summary['contact_info']
                             + '\nАдреса електронної пошти:' + summary['email'])

            check_connections_with_db()
            summary_to_db = {
                'user_id': chat_id,
                'name':  summary['name'],
                'age': summary['age'],
                'faculty': summary['faculty'],
                'specialty': summary['specialty'],
                'course': summary['course'],
                'english_know_lvl': summary['english_know_lvl'],
                'personal_qualities': summary['personal_qualities'],
                'another': summary['another'],
                'experience':  summary['experience'],
                'contact_info': summary['contact_info'],
                'email':  summary['email'],
                'message_id': message_save.message_id
            }
            # Send offer to db
            collection_summary.insert_one(summary_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})

        elif 'summary_cancel' in call.data:
            data = call.data.split(',')
            message_id = call.message.message_id
            chat_id = int(data[1])
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            c = collection_verification.find_one({'message_id': message_id})
            id_object = c['_id']
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='student_choice')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')

            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=chat_id, text='Ваше резюме відхилино!', reply_markup=reply_markup)
            collection_verification.delete_one({"_id": ObjectId("{}".format(id_object))})


        elif 'summary_change' in call.data:  # запускає редагування резюме)
            chat = call.from_user.id
            message_id = call.message.message_id
            summary = collection_verification.find_one({'message_id': message_id})
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            name_change = types.InlineKeyboardButton(
                text="Прізвище, ім’я, по батькові", callback_data='n_a_m_e_change,' + str(summary['_id']))
            age_change = types.InlineKeyboardButton(
                text="Вік", callback_data='age_change,' + str(summary['_id']))
            course_change = types.InlineKeyboardButton(
                text="Курс", callback_data='course_change,' + str(summary['_id']))
            personal_qualities_change = types.InlineKeyboardButton(
                text="Особисті якості", callback_data='pers_quali,' + str(summary['_id']))
            another = types.InlineKeyboardButton(
                text="Інші навички", callback_data='another_change,' + str(summary['_id']))
            experience = types.InlineKeyboardButton(
                text="Досвід роботи", callback_data='experience_change,' + str(summary['_id']))
            keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience)
            bot.send_message(chat, text='Прізвище, ім’я, по батькові: ' + summary['name']
                             + '\nВік: ' + summary['age']
                             + '\nФакультет: ' + summary['faculty']
                             + '\nСпеціальність: ' + summary['specialty']
                             + '\nКурс: ' + summary['course']
                             + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                             + '\nОсобисті якості: ' + summary['personal_qualities']
                             + '\nІнші навички: ' + summary['another']
                             + '\nДосвід роботи: ' + summary['experience']
                             + '\nКонтактний телефон: ' + summary['contact_info']
                             + '\nАдреса електронної пошти: ' + summary['email'])
            bot.send_message(chat, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

        elif 'n_a_m_e_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Прізвище, ім’я, по батькові:')
            bot.register_next_step_handler(msg, n_a_m_e_change)

        elif 'age_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Вік:')
            bot.register_next_step_handler(msg, age_change_progress)

        elif 'course_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Курс:")
            bot.register_next_step_handler(msg, course_change_progress)

        elif 'pers_quali' in call.data:  # редагування контактів студента (НАЗВУ НЕ МІНЯТИ)
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text="Особисті якості:")
            bot.register_next_step_handler(msg, pers_quali_change)

        elif 'another_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text="Інші навички:")
            bot.register_next_step_handler(msg, another_change_progress)

        elif 'experience_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text="Досвід роботи:")
            bot.register_next_step_handler(msg, experience_change_progress)

        elif 'summary_ch_end' in call.data:  # закінчує редагування резюме
            data = call.data.split(',')
            id_object = data[1]
            summary_b = collection_verification.find_one({'_id': ObjectId("{}".format(id_object))})
            user_id = summary_b['user_id']
            print('User id id verif button' + str(call.message.from_user.id))
            bot.delete_message(chat_id=privateChatId, message_id=summary_b['message_id'])
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text='Резюме відредаговано')
            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='end_sum_ch,' + str(user_id) + ',' + str(id_object))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='summary_cancel,' + str(user_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='summary_change,')
            keyboard.add(approve, cancel, change)
            message_save = bot.send_message(privateChatId, text='Прізвище, ім’я, по батькові: ' + summary_b['name']
                                    + '\nВік: ' + summary_b['age']
                                    + '\nФакультет: ' + summary_b['faculty']
                                    + '\nСпеціальність: ' + summary_b['specialty']
                                    + '\nКурс: ' + summary_b['course']
                                    + '\nЗнання англійської мови: ' + summary_b['english_know_lvl']
                                    + '\nОсобисті якості: ' + summary_b['personal_qualities']
                                    + '\nІнші навички: ' + summary_b['another']
                                    + '\nДосвід роботи: ' + summary_b['experience']
                                    + '\nКонтактний телефон: ' + summary_b['contact_info']
                                    + '\nАдреса електронної пошти: ' + summary_b['email'], reply_markup=keyboard)
            collection_verification.update_one({"_id": ObjectId("{}".format(id_object))},
                                               {'$set': {"message_id": message_save.message_id}})

        elif "end_sum_ch" in call.data:  # підтвердження відредагованої резюмешки, перенос документа між колекціями і тд тп
            print(call.data)
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[1])
            obj = data[2]
            summary = collection_verification.find_one({'_id': ObjectId("{}".format(obj))})
            print(user_id, chat_id)
            link = bot.create_chat_invite_link(channelForOffer, member_limit=1)
            c = collection_summary.find_one({'user_id': str(user_id)})
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі резюме", callback_data='get_list_summary')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')

            keyboard = [[choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)

            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме прийнято!' + str(link.invite_link),
                    reply_markup=reply_markup)
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме опубліковано!', reply_markup=reply_markup)
            message_save = bot.send_message(chat_id=channelForSummary, text='Прізвище, ім’я, по батькові: ' + summary['name']
                             + '\nВік: ' + summary['age']
                             + '\nФакультет: ' + summary['faculty']
                             + '\nСпеціальність: ' + summary['specialty']
                             + '\nКурс: ' + summary['course']
                             + '\nЗнання англійської мови: ' + summary['english_know_lvl']
                             + '\nОсобисті якості: ' + summary['personal_qualities']
                             + '\nІнші навички: ' + summary['another']
                             + '\nДосвід роботи: ' + summary['experience']
                             + '\nКонтактний телефон: ' + summary['contact_info']
                             + '\nАдреса електронної пошти: ' + summary['email'])

            check_connections_with_db()
            summary_to_db = {
                'user_id': chat_id,
                'name':  summary['name'],
                'age': summary['age'],
                'faculty': summary['faculty'],
                'specialty': summary['specialty'],
                'course': summary['course'],
                'english_know_lvl': summary['english_know_lvl'],
                'personal_qualities': summary['personal_qualities'],
                'another': summary['another'],
                'experience':  summary['experience'],
                'contact_info': summary['contact_info'],
                'email':  summary['email'],
                'message_id': message_save.message_id
            }
            # Send offer to db
            collection_summary.insert_one(summary_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})

        elif call.data == 'get_list_summary':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            cur = collection_offer.find({'user_id': user_id})
            for doc in cur:
                for x in collection_summary.find():
                    x_split = x['skills'].split()
                    for a in x_split:
                        if a in doc['position']:
                            last = bot.send_message(chat_id, text=form_for_summary_list(x))
                        break
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Список резюме:')

            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі резюме", callback_data='get_list_summary')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                         url=linkToChannelForSummary)
            offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                       url=linkToChannelForOffer)
            keyboard = [[summary_channel, offer_channel], [
                choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=chat_id, text='Ось всі можливі резюме', reply_markup=reply_markup)

            print('Summary List')

        elif call.data == 'get_list_offer':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            skills_summary = collection_summary.find_one({'user_id': user_id})
            for x in collection_offer.find():
                if skills_summary['skills'] in x['position']:
                    last = bot.send_message(chat_id, text=form_for_offer_list(x))
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Список вакансій:')

            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='student_choice')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                         url=linkToChannelForSummary)
            offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                       url=linkToChannelForOffer)

            keyboard = [[summary_channel, offer_channel], [
                choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)

            bot.send_message(
                chat_id, text='Ось всі можливі вакансії (якщо нічого немає, то підходящі вакансії відсутні)', reply_markup=reply_markup)
            print('Offer List')

        elif call.data == 'offer_cal':  # видає вакансії для видалення
            print(call.data)
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            print(user_id)
            offer_search_list = collection_offer.find({'user_id': str(user_id)})
            for x in offer_search_list:
                keyboard_offer = types.InlineKeyboardMarkup()
                delete_offer = types.InlineKeyboardButton(text='Видалити ❌', callback_data='delete_offer,'+str(x['_id'])+','+str(x['message_id']))
                keyboard_offer.add(delete_offer)
                bot.send_message(chat_id, text=form_for_offer_list(x), reply_markup=keyboard_offer)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='student_choice')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                         url=linkToChannelForSummary)
            offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                       url=linkToChannelForOffer)

            keyboard = [[summary_channel, offer_channel], [
                choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)

            bot.send_message(
                chat_id, text='Ось всі ваші вакансії',
                reply_markup=reply_markup)

        elif call.data == 'summary_cal':  # видає резюме для видалення
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            summary_search_list = collection_summary.find({'user_id': int(user_id)})
            for x in summary_search_list:
                keyboard_summary = types.InlineKeyboardMarkup()
                delete_summary = types.InlineKeyboardButton(text='Видалити❌', callback_data='delete_summary,'+str(x['_id'])+','+str(x['message_id']))
                keyboard_summary.add(delete_summary)
                bot.send_message(chat_id, text=form_for_summary_list(x), reply_markup=keyboard_summary)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='student_choice')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                         url=linkToChannelForSummary)
            offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                       url=linkToChannelForOffer)

            keyboard = [[summary_channel, offer_channel], [
                choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)

            bot.send_message(
                chat_id, text='Ось всі ваші резюме',
                reply_markup=reply_markup)

        elif 'delete_offer' in call.data:  # видаляє вакансію
            chat_id = call.message.chat.id
            data = call.data.split(',')
            id_object = data[1]
            message_id = data[2]
            collection_offer.delete_one({"_id": ObjectId("{}".format(id_object))})
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Вакансію видалено')
            bot.delete_message(chat_id=channelForOffer, message_id=message_id)

        elif 'delete_summary' in call.data:  # видаляє резюме
            chat_id = call.message.chat.id
            data = call.data.split(',')
            id_object = data[1]
            message_id = data[2]
            collection_summary.delete_one({"_id": ObjectId("{}".format(id_object))})
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Резюме видалено')
            bot.delete_message(chat_id=channelForSummary, message_id=message_id)

        elif 'fac_st,' in call.data:
            chat_id = call.message.chat.id
            fack = call.data.split(',')
            summary = summary_dict[chat_id]
            markup = types.InlineKeyboardMarkup()
            for keys, value in fac_and_spec.items():
                if fack[1] in keys:
                    summary.faculty = keys
                    for x in value:
                        markup.add(types.InlineKeyboardButton(text=x, callback_data='spec,' + str(x[0:29])))
            bot.send_message(chat_id, text='Спеціальність:', reply_markup=markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)


        elif 'spec,' in call.data:
            chat_id = call.message.chat.id
            summary = summary_dict[chat_id]
            spec = call.data.split(',')
            fac = fac_and_spec
            a = 0
            for value in fac.values():
                for x in value:
                    if spec[1] in x:
                        a = x
            print(a)
            summary.specialty = a
            msg = bot.send_message(chat_id, text='Курс:')
            bot.register_next_step_handler(msg, process_course_step)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif 'english_know' in call.data:
            chat_id = call.message.chat.id
            english_know_lvl = call.data.split(',')
            print(english_know_lvl)
            summary = summary_dict[chat_id]
            summary.english_know_lvl = english_know_lvl[1]
            msg = bot.send_message(chat_id, 'Особисті якості:')
            bot.register_next_step_handler(msg, personal_qualities)
            bot.delete_message(chat_id, message_id=call.message.message_id)

# offer
        elif 'high_school' in call.data:
            chat_id = call.message.chat.id
            data = call.data.split(',')
            high_school = data[1]
            offer = Offer_dict[chat_id]
            offer.high_school = high_school
            markup = types.InlineKeyboardMarkup(row_width=1)
            direction_yes = types.InlineKeyboardButton(text='Так', callback_data='direction_yes')
            direction_no = types.InlineKeyboardButton(text='Ні', callback_data='direction_no')
            markup.add(direction_yes, direction_no)
            bot.send_message(chat_id, text='Вимоги до кандидатів:\nСпеціальність:', reply_markup=markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif call.data == 'direction_yes':
            chat_id = call.message.chat.id
            markup = types.InlineKeyboardMarkup(row_width=1)
            for keys in direction_and_spec.keys():
                markup.add(types.InlineKeyboardButton(text=keys, callback_data='desc_off' + ',' + str(keys[0:25])))
            bot.send_message(chat_id, text='Напрямок:', reply_markup=markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif 'desc_off' in call.data:
            chat_id = call.message.chat.id
            offer = Offer_dict[chat_id]
            data = call.data.split(',')
            desc = data[1]
            for x in direction_and_spec.keys():
                if desc in x:
                    offer.direction = x
            markup = types.InlineKeyboardMarkup(row_width=1)
            eng_lvl_top = types.InlineKeyboardButton(text='Високий рівень',
                                                     callback_data='eng_lvl' + ',' + 'Високий рівень')
            eng_lvl_mid = types.InlineKeyboardButton(text='Середній рівень',
                                                     callback_data='eng_lvl' + ',' + 'Середній рівень')
            eng_lvl_no = types.InlineKeyboardButton(text='Не потрібно',
                                                    callback_data='eng_lvl' + ',' + 'Не потрібно')
            markup.add(eng_lvl_top, eng_lvl_mid, eng_lvl_no)
            bot.send_message(chat_id, text='Вимоги до кандидатів:\nЗнання англійської мови:', reply_markup=markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif call.data == 'direction_no':
            chat_id = call.message.chat.id
            offer = Offer_dict[chat_id]
            offer.direction = 'Ні'
            markup = types.InlineKeyboardMarkup(row_width=1)
            eng_lvl_top = types.InlineKeyboardButton(text='Високий рівень',
                                                     callback_data='eng_lvl' + ',' + 'Високий рівень')
            eng_lvl_mid = types.InlineKeyboardButton(text='Середній рівень',
                                                     callback_data='eng_lvl' + ',' + 'Середній рівень')
            eng_lvl_no = types.InlineKeyboardButton(text='Не потрібно',
                                                    callback_data='eng_lvl' + ',' + 'Не потрібно')
            markup.add(eng_lvl_top, eng_lvl_mid, eng_lvl_no)
            bot.send_message(chat_id, text='Вимоги до кандидатів:\nЗнання англійської мови:', reply_markup=markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif 'eng_lvl' in call.data:
            chat_id = call.message.chat.id
            offer = Offer_dict[chat_id]
            data = call.data.split(',')
            offer.english = data[1]
            msg = bot.send_message(chat_id, text='Вимоги до кандидатів:\nІнші:(вкажіть самостійно)')
            bot.register_next_step_handler(msg, othe_progress)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif 'official_work' in call.data:
            chat_id = call.message.chat.id
            data = call.data.split(',')
            offer = Offer_dict[chat_id]
            offer.official_work = data[1]
            markup = types.InlineKeyboardMarkup(row_width=1)
            remote_job_yes = types.InlineKeyboardButton(text='Так', callback_data='remote_job' + ',' + 'Так')
            remote_job_no = types.InlineKeyboardButton(text='Ні', callback_data='remote_job' + ',' + 'Ні')
            markup.add(remote_job_yes, remote_job_no)
            bot.send_message(chat_id, text='Можливість працювати віддалено:', reply_markup=markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        elif 'remote_job' in call.data:
            chat_id = call.message.chat.id
            data = call.data.split(',')
            offer = Offer_dict[chat_id]
            offer.remote_job = data[1]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Договірна')
            msg = bot.send_message(chat_id, text='Заробітна плата:', reply_markup=markup)
            bot.register_next_step_handler(msg, process_salary)



        else:
            print('wrong callback')
            print(call.data)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(call.message, 'Помилка відправлення в канал...')





def form_for_summary_list(summary):
    name = summary['name']
    age = summary['course']
    faculty = summary['faculty']
    specialty = summary['specialty']
    course = summary['course']
    english_know_lvl = summary['english_know_lvl']
    perso = summary['personal_qualities']
    another = summary['another']
    experience = summary['experience']
    contact_info = summary['contact_info']
    email = summary['email']
    return ('Прізвище, ім’я, по батькові: ' + name + '\nВік: ' + age + '\nФакультет: ' + faculty + '\nСпеціальність: ' + specialty
            + '\nКурс: ' + course + '\nЗнання англійської мови: ' + english_know_lvl + '\nОсобисті якості: ' + str(perso)
            + '\nІнші навички: ' + another + '\nДосвід роботи: ' + experience + '\nКонтактний телефон: ' + contact_info + '\nАдреса електронної пошти: ' + str(email))



def form_for_offer_list(ofr):
    position = ofr['position']
    salary = ofr['salary']
    company_name = ofr['company_name']
    description = ofr['description']
    contact_info = ofr['description']

    return '💼 '+position + '\n💵 '+salary+'\n🏢 '+company_name+'\n📋 ' + description + '\n📞 '+contact_info


def check_connections_with_db():
    try:
        conn = client
        print("Connected successfully!!!")
    except:
        pprint(traceback.format_exc())
        print("Could not connect to MongoDB")



check = check_connections_with_db()
bot.polling(none_stop=True)
