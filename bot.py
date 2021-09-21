# -*- coding: utf-8 -*-
import telebot
from telebot import types
import os
from dotenv import load_dotenv
import traceback
import pymongo
import pprint
from bson.objectid import ObjectId
import datetime
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
direction_and_spec = {'Не важливо': ['Не важливо'],
'Освіта / Педагогіка': ['Дошкільна освіта', 'Початкова освіта ', 'Середня освіта. Українська мова і література ', 'Середня освіта. Українська мова і література ', 'Середня освіта. Англійська мова і література', 'Середня освіта. Німецька мова і література',
'Середня освіта. Французька мова і література', 'Середня освіта. Російська мова і література', 'Середня освіта. Угорська мова і література', 'Середня освіта. Румунська мова і література', 'Середня освіта. Історія', 'Середня освіта. Математика', 'Середня освіта. Біологія та здоров’я людини',
'Середня освіта. Хімія', 'Середня освіта. Географія', 'Середня освіта. Фізика', 'Середня освіта. Фізична культура', 'Спеціальна освіта. Олігофренопедагогіка', 'Фізична культура і спорт'],
'Гуманітарні науки': ['Історія та археологія', 'Філософія', 'Культурологія', 'Філологія. Українська мова і література', 'Філологія. Слов’янські мови та літератури (переклад включно), перша – російська', 'Філологія. Слов’янські мови та літератури (переклад включно), перша –словацька', 'Філологія. Слов’янські мови та літератури (переклад включно), перша –чеська',
'Філологія. Германські мови та літератури (переклад включно), перша – англійська', 'Філологія. Германські мови та літератури (переклад включно), перша – німецька', 'Філологія. Романські мови та літератури (переклад включно), перша – французька', 'Філологія. Угро-фінські мови та літератури (переклад включно), перша – угорська', 'Філологія. Прикладна лінгвістика'],
'Соціальні та поведінкові науки': ['Економіка', 'Політологія', 'Психологія', 'Соціологія'],
'Журналістика': ['Журналістика'],
'Управління та адміністрування': ['Облік і оподаткування', 'Фінанси, банківська справа та страхування', 'Менеджмент', 'Маркетинг', 'Підприємництво, торгівля та біржова діяльність'],
'Право': ['Право'],
'Біологія': ['Біологія'],
'Природничі науки': ['Екологія', 'Хімія', 'Фізика та астрономія', 'Прикладна фізика та наноматеріали', 'Географія'],
'Математика та статистика': ['Математика', 'Прикладна математика'],
'Інформаційні технології': ['Інженерія програмного забезпечення', 'Комп’ютерні науки', 'Комп’ютерна інженерія', 'Системний аналіз', 'Кібербезпека', 'Інформаційні системи та технології'],
'Механічна інженерія': ['Прикладна механіка'],
'Автоматизація та приладобудування': ['Автоматизація та комп’ютерно-інтегровані технології', 'Мікро- та наносистемна техніка'],
'Хімічна та біоінженерія': ['Хімічні технології та інженерія', 'Біомедична інженерія'],
'Електроніка та телекомунікації': ['Електроніка', 'Телекомунікації та радіотехніка'],
'Архітектура та будівництво': ['Будівництво та цивільна інженерія', 'Геодезія та землеустрій'],
'Аграрні науки та продовольство': ['Садівництво та виноградарство', 'Лісове господарство'],
'Охорона здоров’я': ['Стоматологія', 'Медицина', 'Медсестринство. Екстрена медицина', 'Медсестринство. Медсестринство', 'Фармація, промислова фармація', 'Фізична терапія, ерготерапія'],
'Соціальна робота': ['Соціальна робота'],
'Сфера обслуговування': ['Готельно-ресторанна справа', 'Туризм'],
'Цивільна безпека': ['Правоохоронна діяльність'],
'Публічне управління та адміністрування': ['Публічне управління та адміністрування'],
'Міжнародні відносини': ['Міжнародні відносини, суспільні комунікації та регіональні студії', 'Міжнародні економічні відносини', 'Міжнародне право']
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
        bot.send_message(chat_id, text='Офіційне працевлаштування:', reply_markup=markup)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def process_salary(message):
    try:
        chat_id = message.chat.id
        offer = Offer_dict[chat_id]
        salary = message.text
        markup = types.ReplyKeyboardMarkup()
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
        text = '[Згода на використання персональних даних:](https://drive.google.com/file/d/1FlgnpTUsEzFP7lmUcsYG5LB_lih1Dqg8/view?usp=sharing)'
        bot.send_message(chat_id, text=text, parse_mode='MarkdownV2', reply_markup=markup)

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
        bot.send_message(chat_id, text='Факультет:', reply_markup=keyboard)

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
            bot.send_message(chat_id, 'Знання англійської мови:', reply_markup=markup)

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
def comp_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"company_name": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        offer = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        comp_name = types.InlineKeyboardButton(
            text="Назву компанії/установи/організації", callback_data='comp_name_change,' + str(obj))
        vac = types.InlineKeyboardButton(
            text="Вакансію", callback_data='vac_change,' + str(obj))
        salary = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,' + str(obj))
        description = types.InlineKeyboardButton(
            text="Опис вакансії", callback_data='description_change,' + str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,'+str(obj))
        cont = types.InlineKeyboardButton(
            text='Контактні дані', callback_data='offer_cont_in_ch,' + str(obj))
        keyboard.add(comp_name, vac, salary, description, cont, end_change)
        bot.send_message(chat_id, text='Назва компанії/установи/організації: ' + offer['company_name']
                                    + '\nВакансія: ' + offer['vacantion']
                                    + '\nЗакінчена вища освіта: ' + offer['high_school']
                                    + '\nСпеціальність: ' + offer['direction']
                                    + '\nЗнання англійської мови: ' + offer['english']
                                    + '\nІнші вимоги: ' + offer['other']
                                    + '\nОфіційне працевлаштування: ' + offer['official_work']
                                    + '\nМожливість працювати віддалено: ' + offer['remote_job']
                                    + '\nЗаробітна плата: ' + offer['salary']
                                    + '\nБільш детальний опис вакансії: ' + offer['description']
                                    + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)



    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def vac_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"vacantion": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        offer = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        comp_name = types.InlineKeyboardButton(
            text="Назву компанії/установи/організації", callback_data='comp_name_change,' + str(obj))
        vac = types.InlineKeyboardButton(
            text="Вакансію", callback_data='vac_change,' + str(obj))
        salary = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,' + str(obj))
        description = types.InlineKeyboardButton(
            text="Опис вакансії", callback_data='description_change,' + str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,' + str(obj))
        cont = types.InlineKeyboardButton(
            text='Контактні дані', callback_data='offer_cont_in_ch,' + str(obj))
        keyboard.add(comp_name, vac, salary, description, cont, end_change)
        bot.send_message(chat_id, text='Назва компанії/установи/організації: ' + offer['company_name']
                                       + '\nВакансія: ' + offer['vacantion']
                                       + '\nЗакінчена вища освіта: ' + offer['high_school']
                                       + '\nСпеціальність: ' + offer['direction']
                                       + '\nЗнання англійської мови: ' + offer['english']
                                       + '\nІнші вимоги: ' + offer['other']
                                       + '\nОфіційне працевлаштування: ' + offer['official_work']
                                       + '\nМожливість працювати віддалено: ' + offer['remote_job']
                                       + '\nЗаробітна плата: ' + offer['salary']
                                       + '\nБільш детальний опис вакансії: ' + offer['description']
                                       + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])
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
        offer = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        comp_name = types.InlineKeyboardButton(
            text="Назву компанії/установи/організації", callback_data='comp_name_change,' + str(obj))
        vac = types.InlineKeyboardButton(
            text="Вакансію", callback_data='vac_change,' + str(obj))
        salary = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,' + str(obj))
        description = types.InlineKeyboardButton(
            text="Опис вакансії", callback_data='description_change,' + str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,' + str(obj))
        cont = types.InlineKeyboardButton(
            text='Контактні дані', callback_data='offer_cont_in_ch,' + str(obj))
        keyboard.add(comp_name, vac, salary, description, cont, end_change)
        bot.send_message(chat_id, text='Назва компанії/установи/організації: ' + offer['company_name']
                                       + '\nВакансія: ' + offer['vacantion']
                                       + '\nЗакінчена вища освіта: ' + offer['high_school']
                                       + '\nСпеціальність: ' + offer['direction']
                                       + '\nЗнання англійської мови: ' + offer['english']
                                       + '\nІнші вимоги: ' + offer['other']
                                       + '\nОфіційне працевлаштування: ' + offer['official_work']
                                       + '\nМожливість працювати віддалено: ' + offer['remote_job']
                                       + '\nЗаробітна плата: ' + offer['salary']
                                       + '\nБільш детальний опис вакансії: ' + offer['description']
                                       + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])
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
        offer = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        comp_name = types.InlineKeyboardButton(
            text="Назву компанії/установи/організації", callback_data='comp_name_change,' + str(obj))
        vac = types.InlineKeyboardButton(
            text="Вакансію", callback_data='vac_change,' + str(obj))
        salary = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,' + str(obj))
        description = types.InlineKeyboardButton(
            text="Опис вакансії", callback_data='description_change,' + str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,' + str(obj))
        cont = types.InlineKeyboardButton(
            text='Контактні дані', callback_data='offer_cont_in_ch,' + str(obj))
        keyboard.add(comp_name, vac, salary, description, cont, end_change)
        bot.send_message(chat_id, text='Назва компанії/установи/організації: ' + offer['company_name']
                                       + '\nВакансія: ' + offer['vacantion']
                                       + '\nЗакінчена вища освіта: ' + offer['high_school']
                                       + '\nСпеціальність: ' + offer['direction']
                                       + '\nЗнання англійської мови: ' + offer['english']
                                       + '\nІнші вимоги: ' + offer['other']
                                       + '\nОфіційне працевлаштування: ' + offer['official_work']
                                       + '\nМожливість працювати віддалено: ' + offer['remote_job']
                                       + '\nЗаробітна плата: ' + offer['salary']
                                       + '\nБільш детальний опис вакансії: ' + offer['description']
                                       + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])
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
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"description": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        offer = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        comp_name = types.InlineKeyboardButton(
            text="Назву компанії/установи/організації", callback_data='comp_name_change,' + str(obj))
        vac = types.InlineKeyboardButton(
            text="Вакансію", callback_data='vac_change,' + str(obj))
        salary = types.InlineKeyboardButton(
            text="Заробітну плату", callback_data='salary_change,' + str(obj))
        description = types.InlineKeyboardButton(
            text="Опис вакансії", callback_data='description_change,' + str(obj))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='offer_ch_end,' + str(obj))
        cont = types.InlineKeyboardButton(
            text='Контактні дані', callback_data='offer_cont_in_ch,' + str(obj))
        keyboard.add(comp_name, vac, salary, description, cont, end_change)
        bot.send_message(chat_id, text='Назва компанії/установи/організації: ' + offer['company_name']
                                           + '\nВакансія: ' + offer['vacantion']
                                           + '\nЗакінчена вища освіта: ' + offer['high_school']
                                           + '\nСпеціальність: ' + offer['direction']
                                           + '\nЗнання англійської мови: ' + offer['english']
                                           + '\nІнші вимоги: ' + offer['other']
                                           + '\nОфіційне працевлаштування: ' + offer['official_work']
                                           + '\nМожливість працювати віддалено: ' + offer['remote_job']
                                           + '\nЗаробітна плата: ' + offer['salary']
                                           + '\nБільш детальний опис вакансії: ' + offer['description']
                                           + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf,
                     end)
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf,
                     end)
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf,
                     end)
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf,
                     end)
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf,
                     end)
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf,
                     end)
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


def summary_contact_info_changes(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"contact_info": text}})
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
        cont_ibf = types.InlineKeyboardButton(
            text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
        keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience, cont_ibf, end)
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


def clean_collections():
    try:
        now = datetime.datetime.now()
        time_now = now.strftime('%d/%m/%Y')
        for x in collection_offer.find():
            time_parse = datetime.datetime.strptime(x['time'], '%d/%m/%Y')
            time_delta = time_parse + datetime.timedelta(days=2)
            time_delete = time_delta.strftime('%d/%m/%Y')
            time_notification_process = time_parse + datetime.timedelta(days=1)
            time_notification = time_notification_process.strftime('%d/%m/%Y')
            if time_delete == time_now:
                collection_offer.delete_one({'_id': x["_id"]})
                bot.delete_message(chat_id=channelForOffer, message_id=x['message_id'])
            elif time_notification == time_now:
                bot.send_message(chat_id=x['user_id'], text='Через 7 календарних днів вашу вакансію буде видалено')
        for x in collection_summary.find():
            time_parse = datetime.datetime.strptime(x['time'], '%d/%m/%Y')
            time_delta = time_parse + datetime.timedelta(days=2)
            time_delete = time_delta.strftime('%d/%m/%Y')
            time_notification_process = time_parse + datetime.timedelta(days=1)
            time_notification = time_notification_process.strftime('%d/%m/%Y')
            if time_delete == time_now:
                collection_summary.delete_one({'_id': x["_id"]})
                bot.delete_message(chat_id=channelForSummary, message_id=x['message_id'])
            elif time_notification == time_now:
                bot.send_message(chat_id=x['user_id'], text='Через 7 календарних днів ваше резюме буде видалено')
    except Exception as e:
        print(traceback.format_exc())


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
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='new_summary')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')

            keyboard = [[choose, employer_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ви зараз на стороні студента', reply_markup=reply_markup)

        elif call.data == 'employer_choice':
            chat_id = call.message.chat.id
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            keyboard = [[choose, employer_button]]

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
                                  text='\nВаше резюме прийнято для обробки та перевірки. Очікуйте на повідомлення.')
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
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[2])
            now = datetime.datetime.now()
            time = now.strftime('%d/%m/%Y')
            link = bot.create_chat_invite_link(channelForSummary, member_limit=1)
            c = collection_offer.find_one({'user_id': int(user_id)})
            time = datetime.datetime.now()
            time_now = datetime.datetime.strftime(time, '%d/%m/%Y')
            print(user_id, chat_id)
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Видалити вакансію", callback_data='offer_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            res = types.InlineKeyboardButton(text='Підходящі резюме', callback_data='get_list_summary')
            keyboard = [[choose, employer_button], [student_button, res]]
            der = []
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Ваша вакансія прийнята!'
                                          '\nНадсилаємо Вам резюме, які найбільше підходять вимогам вакансії.'
                                          '\nТакож у Вас є можливість ознайомитися з усіма наявними резюме на нашому Каналі з резюме.' + str(link.invite_link))
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваша вакансія прийнята!'
                                          '\nНадсилаємо Вам резюме, які найбільше підходять вимогам вакансії.'
                                          '\nТакож у Вас є можливість ознайомитися з усіма наявними резюме на нашому Каналі з резюме.')
            message_offer_save = bot.send_message(chat_id=channelForOffer, text='Назва компанії/установи/організації: ' + offer['company_name']
                             + '\nВакансія: ' + offer['vacantion']
                             + '\nЗакінчена вища освіта: ' + offer['high_school']
                             + '\nСпеціальність: ' + offer['direction']
                             + '\nЗнання англійської мови: ' + offer['english']
                             + '\nІнші вимоги: ' + offer['other']
                             + '\nОфіційне працевлаштування: ' + offer['official_work']
                             + '\nМожливість працювати віддалено: ' + offer['remote_job']
                             + '\nЗаробітна плата: ' + offer['salary']
                             + '\nБільш детальний опис вакансії: ' + offer['description']
                             + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])

            check_connections_with_db()
            offer_to_db = {
                'user_id': user_id,
                'company_name': offer['company_name'],
                'vacantion': offer['vacantion'],
                'high_school': offer['high_school'],
                'direction': offer['direction'],
                'english': offer['english'],
                'other': offer['other'],
                'official_work': offer['official_work'],
                'remote_job': offer['remote_job'],
                'salary': offer['salary'],
                'description': offer['description'],
                'contact_info': offer['contact_info'],
                'time': time,
                'message_id': message_offer_save.message_id
            }
            # Send offer to db
            collection_offer.insert_one(offer_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})
            for value in collection_offer.find({'user_id': user_id}):
                if value['direction'] in der:
                    continue
                else:
                    for bruch in collection_summary.find():
                        if value['direction'] in bruch['direction']:
                            bot.send_message(chat_id, form_for_summary_list(bruch))
                            der.append(value['direction'])
            bot.send_message(chat_id, text='Підходящі резюме', reply_markup=reply_markup)

        elif 'change_konec,' in call.data:  # закінчує редагування вакансії, копіює вакансію з колекції верифікації в колекцію оффера, постить в канал оффера і видпляє з колекції верифікації
            print(call.data)
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[1])
            obj = data[2]
            offer = collection_verification.find_one({'_id':  ObjectId("{}".format(obj))})
            link = bot.create_chat_invite_link(channelForSummary, member_limit=1)
            c = collection_offer.find_one({'user_id': int(user_id)})
            now = datetime.datetime.now()
            time_now = now.strftime('%d/%m/%Y')
            print(user_id, chat_id)
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Видалити вакансію", callback_data='offer_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            res = types.InlineKeyboardButton(text='Підходящі резюме', callback_data='get_list_summary')
            keyboard = [[choose, employer_button], [student_button, res]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Ваша вакансія прийнята!'
                                          '\nНадсилаємо Вам резюме, які найбільше підходять вимогам вакансії.'
                                          '\nТакож у Вас є можливість ознайомитися з усіма наявними резюме на нашому Каналі з резюме.' + str(link.invite_link))
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваша вакансія прийнята!'
                                          '\nНадсилаємо Вам резюме, які найбільше підходять вимогам вакансії.'
                                          '\nТакож у Вас є можливість ознайомитися з усіма наявними резюме на нашому Каналі з резюме.')
            message_offer_save = bot.send_message(chat_id=channelForOffer,  text='Назва компанії/установи/організації: ' + offer['company_name']
                             + '\nВакансія: ' + offer['vacantion']
                             + '\nЗакінчена вища освіта: ' + offer['high_school']
                             + '\nСпеціальність: ' + offer['direction']
                             + '\nЗнання англійської мови: ' + offer['english']
                             + '\nІнші вимоги: ' + offer['other']
                             + '\nОфіційне працевлаштування: ' + offer['official_work']
                             + '\nМожливість працювати віддалено: ' + offer['remote_job']
                             + '\nЗаробітна плата: ' + offer['salary']
                             + '\nБільш детальний опис вакансії: ' + offer['description']
                             + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])

            check_connections_with_db()
            offer_to_db = {
                'user_id': user_id,
                'company_name': offer['company_name'],
                'vacantion': offer['vacantion'],
                'high_school': offer['high_school'],
                'direction': offer['direction'],
                'english': offer['english'],
                'other': offer['other'],
                'official_work': offer['official_work'],
                'remote_job': offer['remote_job'],
                'salary': offer['salary'],
                'description': offer['description'],
                'contact_info': offer['contact_info'],
                'time': time_now,
                'message_id': message_offer_save.message_id
            }
            # Send offer to db
            collection_offer.insert_one(offer_to_db)
            collection_verification.delete_one({'_id':  ObjectId("{}".format(obj))})
            des = []
            for value in collection_offer.find({'user_id': user_id}):
                if value['direction'] in des:
                    continue
                else:
                    for bruch in collection_summary.find():
                        if value['direction'] in bruch['direction']:
                            bot.send_message(chat_id, form_for_summary_list(bruch))
                            des.append(value['direction'])
            bot.send_message(chat_id, text='Меню', reply_markup=reply_markup)

        elif 'offer_cancel' in call.data:
            message_id = call.message.message_id
            data = call.data.split(',')
            chat_id = int(data[1])
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            c = collection_verification.find_one({'message_id': message_id})
            id_object = c['_id']
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
            collection_verification.delete_one({"_id": ObjectId("{}".format(id_object))})

        elif 'offer_change' in call.data:  # запускає редагування вакансії
            chat = call.from_user.id
            message_id = call.message.message_id
            print(message_id)
            offer = collection_verification.find_one({'message_id': message_id})
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            comp_name = types.InlineKeyboardButton(
                text="Назву компанії/установи/організації", callback_data='comp_name_change,'+str(offer['_id']))
            vac = types.InlineKeyboardButton(
                text="Вакансію", callback_data='vac_change,'+str(offer['_id']))
            salary = types.InlineKeyboardButton(
                text="Заробітну плату", callback_data='salary_change,'+str(offer['_id']))
            description = types.InlineKeyboardButton(
                text="Опис вакансії", callback_data='description_change,'+str(offer['_id']))
            cont = types.InlineKeyboardButton(
                text='Контактні дані', callback_data='offer_cont_in_ch,'+str(offer['_id']))
            keyboard.add(comp_name, vac, salary, description, cont)
            bot.send_message(chat, text='Назва компанії/установи/організації: ' + offer['company_name']
                             + '\nВакансія: ' + offer['vacantion']
                             + '\nЗакінчена вища освіта: ' + offer['high_school']
                             + '\nСпеціальність: ' + offer['direction']
                             + '\nЗнання англійської мови: ' + offer['english']
                             + '\nІнші вимоги: ' + offer['other']
                             + '\nОфіційне працевлаштування: ' + offer['official_work']
                             + '\nМожливість працювати віддалено: ' + offer['remote_job']
                             + '\nЗаробітна плата: ' + offer['salary']
                             + '\nБільш детальний опис вакансії: ' + offer['description']
                             + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'])
            bot.send_message(chat, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

        elif 'comp_name_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Назва компанії/установи/організації:')
            bot.register_next_step_handler(msg, comp_change_progress)

        elif 'vac_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Вакансія:')
            bot.register_next_step_handler(msg, vac_change_progress)

        elif 'salary_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Заробітна плата:')
            bot.register_next_step_handler(msg, salary_change_progress)

        elif 'description_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text='Опис вакансії:')
            bot.register_next_step_handler(msg, description_change_progress)

        elif 'offer_cont_in_ch' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text='Контакти:')
            bot.register_next_step_handler(msg, contact_info_change_progress)

        elif 'offer_ch_end' in call.data:  # це викликається кнопкою "закінчити редагування"
            chat_id = call.message.chat.id
            data = call.data.split(',')
            id_object = data[1]
            offer = collection_verification.find_one({'_id':  ObjectId("{}".format(id_object))})
            user_id = offer['user_id']
            print('User id id verif button' + str(call.message.from_user.id))
            bot.delete_message(chat_id=privateChatId, message_id=offer['message_id'])
            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='change_konec,'+str(user_id)+','+str(id_object))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='offer_cancel,' + str(user_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='offer_change,')
            keyboard.add(approve, cancel, change)
            message_save = bot.send_message(privateChatId,text='Назва компанії/установи/організації: ' + offer['company_name']
                             + '\nВакансія: ' + offer['vacantion']
                             + '\nЗакінчена вища освіта: ' + offer['high_school']
                             + '\nСпеціальність: ' + offer['direction']
                             + '\nЗнання англійської мови: ' + offer['english']
                             + '\nІнші вимоги: ' + offer['other']
                             + '\nОфіційне працевлаштування: ' + offer['official_work']
                             + '\nМожливість працювати віддалено: ' + offer['remote_job']
                             + '\nЗаробітна плата: ' + offer['salary']
                             + '\nБільш детальний опис вакансії: ' + offer['description']
                             + '\nЗа детальною інформацією звертатися: ' + offer['contact_info'], reply_markup=keyboard)
            collection_verification.update_one({"_id": ObjectId("{}".format(id_object))}, {'$set': {"message_id": message_save.message_id}})
            bot.delete_message(chat_id, message_id=call.message.message_id)
            bot.send_message(chat_id, 'Вакансію змінено')

        elif 'summary_verefication' in call.data:
            chat_id = call.message.chat.id
            summary = summary_dict[chat_id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='\nВаше резюме прийнято для обробки та перевірки. Очікуйте на повідомлення')

            print('UserId in sum veref: '+str(chat_id))
            for key, value in direction_and_spec.items():
                for x in value:
                    if summary.specialty in x:
                        print(key)
                        summary.direction = key
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
                'direction': summary.direction,
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
            now = datetime.datetime.now()
            time_now = now.strftime('%d/%m/%Y')
            link = bot.create_chat_invite_link(channelForOffer, member_limit=1)
            c = collection_summary.find_one({'user_id': int(user_id)})
            time = datetime.datetime.now()
            time_now = datetime.datetime.strftime(time, '%d/%m/%Y')
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            student_button = types.InlineKeyboardButton(
                text="Видалити резюме", callback_data='summary_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='new_summary')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            vac = types.InlineKeyboardButton(text='Підходящі вакансії', callback_data='get_list_offer')
            keyboard = [[choose, employer_button], [student_button, vac]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме прийнято!\nНадсилаємо вакансії, які можуть Вас зацікавити.\nТакож у Вас є можливість ознайомитися з усіма наявними '
                                          'вакансіями на нашому Каналі з вакансіями' + str(link.invite_link))
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме прийнято!\nНадсилаємо вакансії, які можуть Вас зацікавити.\nТакож у Вас є можливість ознайомитися з усіма наявними '
                                          'вакансіями на нашому Каналі з вакансіями')

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
                'direction': summary['direction'],
                'email':  summary['email'],
                'time': time_now,
                'message_id': message_save.message_id
            }
            # Send offer to db
            collection_summary.insert_one(summary_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})
            dea = []
            for value in collection_summary.find({'user_id': user_id}):
                if value['direction'] in dea:
                    continue
                else:
                    for bruch in collection_offer.find():
                        if value['direction'] in bruch['direction']:
                            bot.send_message(chat_id, form_for_offer_list(bruch))
                            dea.append(value['direction'])
            bot.send_message(chat_id, text='Меню', reply_markup=reply_markup)

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
            cont_ibf = types.InlineKeyboardButton(
                text='Контактний телефон', callback_data='summary_cont_inf_ch,' + str(summary['_id']))
            keyboard.add(name_change, age_change, course_change, personal_qualities_change, another, experience,
                         cont_ibf)
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

        elif 'pers_quali' in call.data:
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

        elif 'summary_cont_inf_ch' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text="Контактний телефон:")
            bot.register_next_step_handler(msg, summary_contact_info_changes)

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
            now = datetime.datetime.now()
            time_now = now.strftime('%d/%m/%Y')
            link = bot.create_chat_invite_link(channelForOffer, member_limit=1)
            c = collection_summary.find_one({'user_id': str(user_id)})
            time = datetime.datetime.now()
            time_now = datetime.datetime.strftime(time, '%d/%m/%Y')
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Видалити резюме", callback_data='summary_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='new_summary')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            vac = types.InlineKeyboardButton(text='Підходящі вакансії', callback_data='get_list_offer')
            keyboard = [[choose, employer_button], [student_button, vac]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            if c is None:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме прийнято!\nНадсилаємо вакансії, які можуть Вас зацікавити.\nТакож у Вас є можливість ознайомитися з усіма наявними '
                                          'вакансіями на нашому Каналі з вакансіями' + str(link.invite_link))
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме прийнято!\nНадсилаємо вакансії, які можуть Вас зацікавити.\nТакож у Вас є можливість ознайомитися з усіма наявними '
                                          'вакансіями на нашому Каналі з вакансіями\n')
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
                'direction': summary['direction'],
                'email':  summary['email'],
                'time': time_now,
                'message_id': message_save.message_id
            }
            # Send offer to db
            collection_summary.insert_one(summary_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})
            deb = []
            for value in collection_summary.find({'user_id': user_id}):
                if value['direction'] in deb:
                    continue
                else:
                    for bruch in collection_offer.find():
                        if value['direction'] in bruch['direction']:
                            bot.send_message(chat_id, form_for_offer_list(bruch))
                            deb.append(value['direction'])
            bot.send_message(chat_id, text='Меню', reply_markup=reply_markup)

        elif call.data == 'get_list_summary':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            deb = []
            for value in collection_offer.find({'user_id': user_id}):
                if value['direction'] in deb:
                    continue
                else:
                    for bruch in collection_summary.find():
                        if value['direction'] in bruch['direction']:
                            bot.send_message(chat_id, form_for_summary_list(bruch))
                            deb.append(value['direction'])
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Список резюме:')
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Видалити вакансію", callback_data='offer_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            resume = types.InlineKeyboardButton(text='Підходящі резюме', callback_data='get_list_summary')
            keyboard = [[choose, employer_button], [student_button, resume]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=chat_id, text='Меню', reply_markup=reply_markup)

            print('Summary List')

        elif call.data == 'get_list_offer':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            deb = []
            for value in collection_summary.find({'user_id': user_id}):
                if value['direction'] in deb:
                    continue
                else:
                    for bruch in collection_offer.find():
                        if value['direction'] in bruch['direction']:
                            bot.send_message(chat_id, form_for_offer_list(bruch))
                            deb.append(value['direction'])
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Список вакансій:')
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Видалити резюме", callback_data='summary_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='new_summary')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            vacant = types.InlineKeyboardButton(text='Підходящі вакансії', callback_data='get_list_offer')
            keyboard = [[choose, employer_button], [student_button, vacant]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id, text='Меню', reply_markup=reply_markup)
            print('Offer List')

        elif call.data == 'offer_cal':  # видає вакансії для видалення
            print(call.data)
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            print(user_id)
            offer_search_list = collection_offer.find({'user_id': int(user_id)})
            for x in offer_search_list:
                keyboard_offer = types.InlineKeyboardMarkup()
                delete_offer = types.InlineKeyboardButton(text='Видалити ❌', callback_data='delete_offer,'+str(x['_id'])+','+str(x['message_id']))
                keyboard_offer.add(delete_offer)
                bot.send_message(chat_id, text=form_for_offer_list(x), reply_markup=keyboard_offer)
            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Видалити вакансію", callback_data='offer_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нова вакансія", callback_data='new_offer')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            resume = types.InlineKeyboardButton(text='Підходящі резюме', callback_data='get_list_summary')
            keyboard = [[choose, employer_button], [student_button, resume]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id, text='Ось всі ваші вакансії',
                reply_markup=reply_markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

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
                text="Видалити резюме", callback_data='summary_cal')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='new_summary')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            vacant = types.InlineKeyboardButton(text='Підходящі вакансії', callback_data='get_list_offer')
            keyboard = [[choose, employer_button], [student_button, vacant]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id, text='Меню',
                reply_markup=reply_markup)
            bot.delete_message(chat_id, message_id=call.message.message_id)

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
#summary
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
            for keys in direction_and_spec.keys():
                markup.add(types.InlineKeyboardButton(text=keys, callback_data='desc_off' + ',' + str(keys[0:25])))
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
            msg = bot.send_message(chat_id, text='Заробітна плата:')
            bot.register_next_step_handler(msg, process_salary)
            bot.delete_message(chat_id, message_id=call.message.message_id)

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
    com_nam = ofr['company_name']
    va = ofr['vacantion']
    high_school = ofr['high_school']
    direction = ofr['direction']
    english = ofr['english']
    other = ofr['other']
    official_work = ofr['official_work']
    remote_job = ofr['remote_job']
    salary = ofr['salary']
    description = ofr['description']
    contact_inf = ofr['contact_info']

    return ('Назва компанії/установи/організації: ' + com_nam + '\nВакансія: ' + va + '\nЗакінчена вища освіта: ' + high_school + '\nСпеціальність: ' + direction
            + '\nЗнання англійської мови: ' + english + '\nІнші вимоги: ' + other + '\nОфіційне працевлаштування: ' + official_work
            + '\nМожливість працювати віддалено: ' + remote_job + '\nЗаробітна плата: ' + salary + '\nБільш детальний опис вакансії: ' + description + '\nЗа детальною інформацією звертатися: ' + contact_inf)


def check_connections_with_db():
    try:
        conn = client
        print("Connected successfully!!!")
    except:
        pprint(traceback.format_exc())
        print("Could not connect to MongoDB")

if __name__=="__main__":
    check = check_connections_with_db()
    bot.polling(none_stop=True)