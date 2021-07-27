import telebot
from telebot import types
import os
from dotenv import load_dotenv
import traceback
import pymongo
import pprint
from bson.objectid import ObjectId
load_dotenv()

bot = telebot.TeleBot('1870782408:AAFgZcSZCPTS_X9O0ckjUWbjr2FfhFjQTp4')


class Offer:
    def __init__(self, position):
        self.position = position
        self.salary = None
        self.company_name = None
        self.description = None
        self.contact_info = None


class Summary:
    def __init__(self, skills):
        self.skills = skills
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
botDesctiption = os.getenv('BOT_DESCRIPTION')

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

        bot.reply_to(message, botDesctiption, reply_markup=start_keyboard)
        keyboard = types.InlineKeyboardMarkup()
        student_choice = types.InlineKeyboardButton(
            text="Студент", callback_data='student_choice')
        employer_choice = types.InlineKeyboardButton(
            text="Роботодавець", callback_data='employer_choice')

        print('USER ID:'+str(message.from_user.id))

        keyboard.add(student_choice, employer_choice)

        bot.reply_to(message, 'Ви студент чи роботодавець?',
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
            bot.register_next_step_handler(msg, process_skills_step)
            return

        elif message.text == employer_const:
            msg = bot.reply_to(message, 'Введіть будь ласка посаду:')
            bot.register_next_step_handler(msg, process_position_step)
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
def process_position_step(message):
    try:
        chat_id = message.chat.id
        print('Chat id: '+str(chat_id))
        print('User id in pos stet'+str(message.from_user.id))

        position = message.text
        offer = Offer(position)
        Offer_dict[chat_id] = offer
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Договірна')
        msg = bot.reply_to(
            message, 'Введіть заробітну плату', reply_markup=markup)
        bot.register_next_step_handler(msg, process_salary_step)
    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def process_salary_step(message):
    try:
        chat_id = message.chat.id
        offer = Offer_dict[chat_id]
        salary = message.text
        markup = types.ReplyKeyboardRemove()
        if not salary.isdigit() and salary != 'Договірна':
            msg = bot.reply_to(
                message, 'Заробітна плата повинна бути числом.Введіть заробітну плату(якщо 0 то договірна)')
            bot.register_next_step_handler(msg, process_salary_step)
            return
        if(salary == 0):
            offer.salary = 'Договірна'
        offer.salary = salary
        msg = bot.reply_to(message, 'Введіть назву компанії',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_company_name_step)
    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def process_company_name_step(message):
    try:
        chat_id = message.chat.id
        company_name = message.text
        offer = Offer_dict[chat_id]
        offer.company_name = company_name
        msg = bot.reply_to(message, 'Опишіть вакансію більш детально')
        bot.register_next_step_handler(msg, process_description_step)
    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'oooops')


def process_description_step(message):
    try:
        chat_id = message.chat.id
        description = message.text
        offer = Offer_dict[chat_id]
        offer.description = description

        msg = bot.reply_to(
            message, 'Введіть контактну інформацію для звізку з вами')
        bot.register_next_step_handler(msg, process_contact_info_step)

    except Exception as e:
        bot.reply_to(message, 'Опис вакансії ')


def process_contact_info_step(message):
    try:
        chat_id = message.chat.id
        contact_info = message.text
        offer = Offer_dict[chat_id]
        offer.contact_info = contact_info

        keyboard = types.InlineKeyboardMarkup()
        send_button = types.InlineKeyboardButton(
            text="Верифікувати", callback_data='offer_verefication,'+str(message.from_user.id))
        keyboard.add(send_button)

        msg = bot.send_message(chat_id, text='Ваша пропозиція буде виглядати ось так:'
                               + '\n\n💼 ' + offer.position
                               + '\n💵 ' + offer.salary
                               + '\n🏢 ' + offer.company_name
                               + '\n📋 ' + offer.description
                               + '\n📞 ' + offer.contact_info, reply_markup=keyboard)

    except Exception as e:
        print(e)
        bot.reply_to(
            message, 'Помилка зчитування контактної інформації чи що там...')


'''
# Student Section
'''
def process_skills_step(message):
    try:
        chat_id = message.chat.id
        skills = message.text
        summary = Summary(skills)
        summary_dict[chat_id] = summary

        msg = bot.reply_to(
            message, 'Введіть курс на якому ви навчаєтесь (1-6)')
        bot.register_next_step_handler(msg, process_course_step)
    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка в зчитуванні курса...')


def process_course_step(message):
    try:
        chat_id = message.chat.id
        course = int(message.text)
        if course > 0 and course < 7:
            summary = summary_dict[chat_id]
            summary.course = str(course)
            msg = bot.reply_to(message, 'Введіть Призвіще Ім`я По батькові')
            bot.register_next_step_handler(
                msg, process_fist_name_last_name_step)
        else:
            msg = bot.reply_to(message, 'Введіть курс коректтно.')
            bot.register_next_step_handler(msg, process_course_step)

    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка в зчитувані курса...')


def process_fist_name_last_name_step(message):
    try:
        chat_id = message.chat.id
        fnlt = message.text
        summary = summary_dict[chat_id]
        summary.first_name_last_name = fnlt
        msg = bot.reply_to(message, 'Введіть контактні данні')
        bot.register_next_step_handler(msg, process_student_contact_info_step)
    except Exception as e:
        print(Exception(e))
        bot.reply_to(message, 'Помилка в зчитуванні контактів...')


def process_student_contact_info_step(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        contact_info = message.text
        summary = summary_dict[chat_id]
        summary.contact_info = contact_info

        keyboard = types.InlineKeyboardMarkup()
        send_button = types.InlineKeyboardButton(
            text="Верифікувати", callback_data='summary_verefication,'+str(user_id))
        keyboard.add(send_button)

        bot.send_message(chat_id, text='Ваше резюме буде виглядати ось так:'
                         + '\n\n💻 ' + summary.skills
                         + '\n🎓 ' + summary.course
                         + '\n📋 ' + summary.first_name_last_name
                         + '\n📞 ' + summary.contact_info, reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'Помилка в публікації остаточного варіанту...')

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


def skills_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"skills": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        skills_change = types.InlineKeyboardButton(
            text="Мову", callback_data='skills_change,' + str(change['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(change['_id']))
        first_name_last_name_change = types.InlineKeyboardButton(
            text="Ім'я та прізвище", callback_data='name_last_change,' + str(change['_id']))
        contact_info_change = types.InlineKeyboardButton(
            text="Контакти", callback_data='scc,' + str(change['_id']))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(obj))
        keyboard.add(skills_change, course_change, first_name_last_name_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💻 ' + change_1['skills']
                                    + '\n🎓 ' + change_1['course']
                                    + '\n📋 ' + change_1['first_name_last_name']
                                    + '\n📞 ' + change_1['contact_info'])
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
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        skills_change = types.InlineKeyboardButton(
            text="Мову", callback_data='skills_change,' + str(change['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(change['_id']))
        first_name_last_name_change = types.InlineKeyboardButton(
            text="Ім'я та прізвище", callback_data='name_last_change,' + str(change['_id']))
        contact_info_change = types.InlineKeyboardButton(
            text="Контакти", callback_data='scc,' + str(change['_id']))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(obj))
        keyboard.add(skills_change, course_change, first_name_last_name_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💻 ' + change_1['skills']
                                    + '\n🎓 ' + change_1['course']
                                    + '\n📋 ' + change_1['first_name_last_name']
                                    + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def first_name_last_name_change_progress(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        change = collection_verification.find_one({'change_id': user_id})
        obj = change["_id"]
        collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {'$set': {"first_name_last_name": text}})
        bot.send_message(chat_id, text='Зміни внесено')
        change_1 = collection_verification.find_one({'change_id': user_id})
        keyboard = types.InlineKeyboardMarkup()
        skills_change = types.InlineKeyboardButton(
            text="Мову", callback_data='skills_change,' + str(change['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(change['_id']))
        first_name_last_name_change = types.InlineKeyboardButton(
            text="Ім'я та прізвище", callback_data='name_last_change,' + str(change['_id']))
        contact_info_change = types.InlineKeyboardButton(
            text="Контакти", callback_data='scc,' + str(change['_id']))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(obj))
        keyboard.add(skills_change, course_change, first_name_last_name_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💻 ' + change_1['skills']
                                    + '\n🎓 ' + change_1['course']
                                    + '\n📋 ' + change_1['first_name_last_name']
                                    + '\n📞 ' + change_1['contact_info'])
        bot.send_message(chat_id, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, 'біда')


def summary_contact_change(message):
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
        skills_change = types.InlineKeyboardButton(
            text="Мову", callback_data='skills_change,' + str(change['_id']))
        course_change = types.InlineKeyboardButton(
            text="Курс", callback_data='course_change,' + str(change['_id']))
        first_name_last_name_change = types.InlineKeyboardButton(
            text="Ім'я та прізвище", callback_data='name_last_change,' + str(change['_id']))
        contact_info_change = types.InlineKeyboardButton(
            text="Контакти", callback_data='scc,' + str(change['_id']))
        end_change = types.InlineKeyboardButton(
            text='Закінчити редагування', callback_data='summary_ch_end,' + str(obj))
        keyboard.add(skills_change, course_change, first_name_last_name_change, contact_info_change, end_change)
        bot.send_message(chat_id, text='💻 ' + change_1['skills']
                                    + '\n🎓 ' + change_1['course']
                                    + '\n📋 ' + change_1['first_name_last_name']
                                    + '\n📞 ' + change_1['contact_info'])
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
            msg = bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Введіть мови програмування які ви знаєте:')

            bot.register_next_step_handler(msg, process_skills_step)

        elif call.data == 'new_offer':
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Введіть будь ласка посаду:')

            bot.register_next_step_handler(msg, process_position_step)

        elif 'offer_verefication' in call.data:
            data = call.data.split(',')
            chat_id = call.message.chat.id
            user_id = data[1]
            offer = Offer_dict[chat_id]
            print('User id id verif button'+str(call.message.from_user.id))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='\nПісля верифікації її можна буде переглянути в каналі\n\n' + channelForOffer)
            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='offer_approve,'+str(chat_id)+','+str(user_id))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='offer_cancel,'+str(chat_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='offer_change,')
            keyboard.add(approve, cancel, change)
            message_save = bot.send_message(chat_id=privateChatId, text='💼 ' + offer.position
                             + '\n💵 ' + offer.salary
                             + '\n🏢 ' + offer.company_name
                             + '\n📋 ' + offer.description
                             + '\n📞 ' + offer.contact_info, reply_markup=keyboard)

            check_connections_with_db()
            offer_to_db = {
                'user_id': user_id,
                'position': offer.position,
                'salary': offer.salary,
                'company_name': offer.company_name,
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
            data = call.data.split(',')
            chat_id = call.message.chat.id
            user_id = data[1]
            summary = summary_dict[chat_id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='\nПісля верифікації його можна буде переглянути в каналі\n\n' + channelForSummary)

            print('UserId in sum veref: '+str(user_id))

            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='summary_approve,'+str(chat_id)+','+str(user_id))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='summary_cancel,'+str(chat_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='summary_change,')
            keyboard.add(approve, cancel, change)
            message_summary_save = bot.send_message(chat_id=privateChatId, text='\n\n💻 ' + summary.skills
                             + '\n🎓 ' + summary.course
                             + '\n📋 ' + summary.first_name_last_name
                             + '\n📞 ' + summary.contact_info, reply_markup=keyboard)

            check_connections_with_db()
            summary_to_db = {
                'user_id': user_id,
                'skills': summary.skills,
                'course': summary.course,
                'first_name_last_name': summary.first_name_last_name,
                'contact_info': summary.contact_info,
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
            c = collection_summary.find_one({'user_id': str(user_id)})
            print(summary['skills'])
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

            message_save = bot.send_message(chat_id=channelForSummary, text='\n\n💻 ' + summary['skills']
                             + '\n🎓 ' + summary['course']
                             + '\n📋 ' + summary['first_name_last_name']
                             + '\n📞 ' + summary['contact_info'])

            check_connections_with_db()
            summary_to_db = {
                'user_id': summary['user_id'],
                'skills': summary['skills'],
                'course': summary['course'],
                'first_name_last_name': summary['first_name_last_name'],
                'contact_info': summary['contact_info'],
                'message_id': message_save.message_id
            }
            # Send offer to db
            collection_summary.insert_one(summary_to_db)
            collection_verification.delete_one({'_id': ObjectId("{}".format(obj))})

        elif 'summary_cancel' in call.data:
            data = call.data.split(',')
            chat_id = int(data[1])
            summary = summary_dict[chat_id]
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
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

        elif 'summary_change' in call.data:  # запускає редагування резюме)
            chat = call.from_user.id
            message_id = call.message.message_id
            print(message_id)
            change = collection_verification.find_one({'message_id': message_id})
            keyboard = types.InlineKeyboardMarkup()
            skills_change = types.InlineKeyboardButton(
                text="Мову програмування", callback_data='skills_change,' + str(change['_id']))
            course_change = types.InlineKeyboardButton(
                text="Курсу", callback_data='course_change,' + str(change['_id']))
            first_name_last_name_change = types.InlineKeyboardButton(
                text="Ім'я та прізвище", callback_data='name_last_change,' + str(change['_id']))
            contact_info_change = types.InlineKeyboardButton(
                text="Контакти", callback_data='scc,' + str(change['_id']))
            keyboard.add(skills_change, course_change, first_name_last_name_change, contact_info_change)
            bot.send_message(chat, text='💻 ' + change['skills']
                                        + '\n🎓 ' + change['course']
                                        + '\n📋 ' + change['first_name_last_name']
                                        + '\n📞 ' + change['contact_info'])
            bot.send_message(chat, text='Обріть, що бажаєте змінити:', reply_markup=keyboard)

        elif 'skills_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Введіть мову:')
            bot.register_next_step_handler(msg, skills_change_progress)

        elif 'course_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='Введіть курс:')
            bot.register_next_step_handler(msg, course_change_progress)

        elif 'name_last_change' in call.data:
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Введіть ім'я та прізвище:")
            bot.register_next_step_handler(msg, first_name_last_name_change_progress)

        elif 'scc' in call.data:  # редагування контактів студента (НАЗВУ НЕ МІНЯТИ)
            user_id = call.message.chat.id
            data = call.data.split(',')
            obj = data[1]
            print(user_id)
            print(obj)
            collection_verification.update_one({"_id": ObjectId("{}".format(obj))}, {"$set": {'change_id': user_id}})
            chat_id = call.message.chat.id
            msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                        text="Введіть контакти:")
            bot.register_next_step_handler(msg, summary_contact_change)

        elif 'summary_ch_end' in call.data:  # закінчує редагування резюме
            data = call.data.split(',')
            id_object = data[1]
            summary_b = collection_verification.find_one({'_id': ObjectId("{}".format(id_object))})
            user_id = summary_b['user_id']
            print('User id id verif button' + str(call.message.from_user.id))
            bot.delete_message(chat_id=privateChatId, message_id=summary_b['message_id'])
            keyboard = types.InlineKeyboardMarkup()
            approve = types.InlineKeyboardButton(
                text="Підтвердити", callback_data='end_sum_ch,' + str(user_id) + ',' + str(id_object))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='summary_cancel,' + str(user_id))
            change = types.InlineKeyboardButton(
                text='Редагувати', callback_data='summary_change,')
            keyboard.add(approve, cancel, change)
            message_save = bot.send_message(privateChatId, text='💻 ' + summary_b['skills']
                                                                + '\n🎓 ' + summary_b['course']
                                                                + '\n📋 ' + summary_b['first_name_last_name']
                                                                + '\n📞 ' + summary_b['contact_info'],
                                            reply_markup=keyboard)
            collection_verification.update_one({"_id": ObjectId("{}".format(id_object))},
                                               {'$set': {"message_id": message_save.message_id}})

        elif "end_sum_ch" in call.data:  # підтвердження відредагованої резюмешки, перенос документа між колекціями і тд тп
            print(call.data)
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[1])
            obj = data[2]
            summary_vacantion = collection_verification.find_one({'_id': ObjectId("{}".format(obj))})
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
                    chat_id=chat_id, text='Ваше резюме опубліковано!' + str(link.invite_link),
                    reply_markup=reply_markup)
            else:
                bot.send_message(
                    chat_id=chat_id, text='Ваше резюме опубліковано!', reply_markup=reply_markup)
            message_offer_save = bot.send_message(chat_id=channelForSummary, text='💻 ' + summary_vacantion["skills"]
                                                                                + '\n🎓 ' + summary_vacantion[
                                                                                    "course"]
                                                                                + '\n📋 ' + summary_vacantion[
                                                                                    'first_name_last_name']
                                                                                + '\n📞 ' + summary_vacantion[
                                                                                    'contact_info'])

            check_connections_with_db()
            summary_to_db = {
                'user_id': summary_vacantion['user_id'],
                'skills': summary_vacantion['skills'],
                'course': summary_vacantion['course'],
                'first_name_last_name': summary_vacantion['first_name_last_name'],
                'contact_info': summary_vacantion['contact_info'],
                'message_id': message_offer_save.message_id
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
            summary_search_list = collection_summary.find({'user_id': str(user_id)})
            for x in summary_search_list:
                keyboard_summary = types.InlineKeyboardMarkup()
                edit_summary = types.InlineKeyboardButton(text='Змінити ✏', callback_data='edit_summary,'+str(x['_id'])+','+str(x['message_id']))
                delete_summary = types.InlineKeyboardButton(text='Видалити❌', callback_data='delete_summary,'+str(x['_id'])+','+str(x['message_id']))
                keyboard_summary.add(edit_summary, delete_summary)
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

        else:
            print('wrong callback')
            print(call.data)

    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(call.message, 'Помилка відправлення в канал...')





def form_for_summary_list(summary):
    skills = summary['skills']
    course = summary['course']
    first_name_last_name = summary['first_name_last_name']
    contact_info = summary['contact_info']

    return '💻 ' + skills + '\n🎓 ' + course + '\n📋 ' + first_name_last_name + '\n📞 ' + contact_info,


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
