from logging import exception
import telebot as telebot
from telebot import types
import traceback
import pymongo
import pprint

# ПРОВЕРКА СВЯЗі

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
who_am_i = ''
student_const = 'Студент'
employer_const = 'Роботодавець'
privateChatId = -1001243179442
channelForSummary = '@channelForSummary'
channelForOffer = '@chennalForVacation'

# Vlad DB mongodb+srv://admin:admin@cluster0.b6p5p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0.h4nf9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db_name = 'Tel_Bot_Uzhnu'
collection_offer = client[db_name]['Offer']
collection_summary = client[db_name]['Summary']

# Handle '/start' and '/help'


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    try:
        start_keyboard = types.InlineKeyboardMarkup()
        summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                     url="https://t.me/channelForSummary")
        offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                   url="https://t.me/chennalForVacation")
        start_keyboard.add(summary_channel, offer_channel)

        bot.reply_to(message, """\
        Доброго дня це Бот для пошуку вакансій та розміщення резюме  для математиків.
Щоб розмістити пропозицію такі поля:
💼 Посада.
💵 Заробітна плата(якщо 0 то договірна).
🏢 Назва компанії.
📋 Більш детальний опис пропозиції.
        """, reply_markup=start_keyboard)
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
        who_am_i = message.text

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
# Handle '/new_offer


@bot.message_handler(commands=['new_offer'])
def new_offer(message):
    chat_id = message.chat.id
    position = message.text
    offer = Offer(position)
    Offer_dict[chat_id] = offer

    chat_id = message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id)
    msg = bot.reply_to(message, 'Введіть будь ласка посаду:')
    bot.register_next_step_handler(msg, process_position_step)


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
                text="Підтвердити", callback_data='offer_approve,'+str(chat_id)+','+str(call.message.from_user.id))
            cancel = types.InlineKeyboardButton(
                text="Відхилити", callback_data='offer_cancel,'+str(chat_id))

            keyboard.add(approve, cancel)

            bot.send_message(chat_id=privateChatId, text='💼 ' + offer.position
                             + '\n💵 ' + offer.salary
                             + '\n🏢 ' + offer.company_name
                             + '\n📋 ' + offer.description
                             + '\n📞 ' + offer.contact_info, reply_markup=keyboard)

        elif 'offer_approve' in call.data:
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[2])
            offer = Offer_dict[chat_id]
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

            check_connections_with_db()
            offer_to_db = {
                'user_id': user_id,
                'position': offer.position,
                'salary': offer.salary,
                'company_name': offer.company_name,
                'description': offer.description,
                'contact_info': offer.contact_info,
            }
            # Send offer to db
            collection_offer.insert_one(offer_to_db)

            bot.send_message(
                chat_id=chat_id, text='Вашу вакансію опубліковано!', reply_markup=reply_markup)
            bot.send_message(chat_id=channelForOffer, text='💼 ' + offer.position
                             + '\n💵 ' + offer.salary
                             + '\n🏢 ' + offer.company_name
                             + '\n📋 ' + offer.description
                             + '\n📞 ' + offer.contact_info)

        elif 'offer_cancel' in call.data:
            data = call.data.split(',')
            chat_id = int(data[1])
            offer = Offer_dict[chat_id]
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
                chat_id=chat_id, text='Вашу вакансію відхилино!', reply_markup=reply_markup)

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
            keyboard.add(approve, cancel)
            bot.send_message(chat_id=privateChatId, text='\n\n💻 ' + summary.skills
                             + '\n🎓 ' + summary.course
                             + '\n📋 ' + summary.first_name_last_name
                             + '\n📞 ' + summary.contact_info, reply_markup=keyboard)

        elif 'summary_approve' in call.data:
            data = call.data.split(',')
            chat_id = int(data[1])
            user_id = int(data[2])
            summary = summary_dict[chat_id]
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

            check_connections_with_db()
            summary_to_db = {
                'user_id': user_id,
                'skills': summary.skills,
                'course': summary.course,
                'first_name_last_name': summary.course,
                'contact_info': summary.contact_info,
            }
            # Send summary to db
            collection_summary.insert_one(summary_to_db)

            bot.send_message(
                chat_id=chat_id, text='Ваше резюме опубліковано!', reply_markup=reply_markup)

            bot.send_message(chat_id=channelForSummary, text='\n\n💻 ' + summary.skills
                             + '\n🎓 ' + summary.course
                             + '\n📋 ' + summary.first_name_last_name
                             + '\n📞 ' + summary.contact_info)

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

        elif call.data == 'get_list_summary':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            user_offer = collection_offer.find({'user_id': user_id})

            for x in collection_summary.find():
                last = bot.send_message(chat_id, text=form_for_summary_list(x))

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
                                                         url="https://t.me/channelForSummary")
            offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                       url="https://t.me/chennalForVacation")
            keyboard = [[summary_channel, offer_channel], [
                choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=chat_id, text='Ось всі можливі резюме', reply_markup=reply_markup)

            print('Summary List')

        elif call.data == 'get_list_offer':
            chat_id = call.message.chat.id
            user_id = call.from_user.id

            user_summary = collection_summary.find_one({'user_id': user_id})
            pprint.pprint(user_summary['skills'])

            for x in collection_offer.find({}):
                last = bot.send_message(chat_id, text=form_for_offer_list(x))

            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id, text='Список вакансій:')

            keyboard = types.InlineKeyboardMarkup()
            student_button = types.InlineKeyboardButton(
                text="Переглянути можливі вакансії", callback_data='get_list_offer')
            employer_button = types.InlineKeyboardButton(
                text="Нове резюме", callback_data='student_choice')
            choose = types.InlineKeyboardButton(
                text="Зміна перегляду", callback_data='who_am_i')
            summary_channel = types.InlineKeyboardButton(text='Канал з резюме',
                                                         url="https://t.me/channelForSummary")
            offer_channel = types.InlineKeyboardButton(text='Канал з вакансіями',
                                                       url="https://t.me/chennalForVacation")

            keyboard = [[summary_channel, offer_channel], [
                choose, employer_button], [student_button]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)

            bot.send_message(
                chat_id, text='Ось всі можливі вакансії', reply_markup=reply_markup)
            print('Offer List')

        else:
            print('wrong callback')
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


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)
check = check_connections_with_db()
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()

bot.polling(none_stop=True)
