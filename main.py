import time
import yoomoney
import telebot
import pandas as pd
import re
import threading
import numpy as np
import pytz

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from yoomoney import Quickpay
from yoomoney import Client

from datetime import datetime
from datetime import timedelta
from threading import Timer

bot = telebot.TeleBot('5423176144:AAEAHewAvanY5W4ImVC7P3RoPzlkAdzG0wA')
yoomoney_token = "4100117805460248.11EA3C4E3C9C83223569E5AC97BB3021B91BF3223716AF874F39B444D9FC3BD60D5D0EA790F537779AF123D171566090201CCEB73D2B956B925E2E7C95F7CD781C7894BF3C7549CB55D93FCD6E7AEB36F86AFBCE9747845968DB0D6794A548702838EB302925667B83BA85CFBC1F6234EB89C99BECBD15EF60CBB265D7BFFCEB"
client = Client(yoomoney_token)

# session_list_csv = pd.read_csv('session_list.csv', sep='\t')
session_list_dic = {
    'psycodynamic':
        {'name':"Психодинамическая группа",
         'date_time':"по четвергам, 20:00 МСК",
         'reminder':"3_20:00",
         'specialist':"Фёдор Коньков",
         'picture':"NULL",
         'description':"Продолжительность - 10 недель",
         'invite': f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':15,
         'members':{},
         'queue':{}},
    'volunteertraining':
        {'name':"Группа поддержки для тех, кто помогает другим профессионально или как волонтёр",
         'date_time':"раз в неделю, 10 недель",
         'reminder':"",
         'specialist':"Фёдор Коньков",
         'picture':"NULL",
         'description':"* Выгорание - как избежать и что делать если оно вас настигло\n"
                       "* Сапожник без сапог - как научиться заботиться о себе, даже если вы хорошо умеете заботиться о других\n"
                       "* Проекция - как избежать видеть себя в клиенте\n"
                       "* Эмпатия - когда она помогает, а когда мешает\n"
                       "* Границы - как то что мы не делаем и не позволяем себе и другим может помогать вам и другим добиться хороших долговременных результатов\n"
                       "* Также психологи ответят на различные ваши вопросы о том как помогать эффективно и безопасно для всех\n\n"
                       "* Фокус - как позитивно и эффективно пережить перемены в ситуации неопределенности, открыть новые горизонты в себе, окружающих, и мире.\n\n"
                       "* Активный бмен личным опытом, чувствами, переживаниями. Возможность получить поддержку, обратную связь, новые навыки, в доброжелательный обстановке.\n\n"
                       "* Психолог поможет создать безопасную, свободную и творчесткую атмосферу для достижения группой и каждым участником максимального позитивных результатов. Полученный опыт, навыки и знания помогут с существующими и предстоящими жизненными ситуациями.",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':20,
         'members':{},
         'queue':{}},
    'meditation':
        {'name':"Медитация",
         'date_time':"по понедельникам, 21:30 МСК",
         'reminder':"0_21:30",
         'specialist':"Надежда Серебряникова",
         'picture':"NULL",
         'description':"Продолжительность - 10 недель",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':20,
         'members':{},
         'queue':{}},
    'metoday':
        {'name':"Группа для подростков 13-15 лет \"Я сегодня\"",
         'date_time':"по понедельникам, 19:00 МСК",
         'reminder':"0_19:00",
         'specialist':"Надежда Серебряникова",
         'picture':"NULL",
         'description':"Это группа для детей, которые  после переезда:\n"
                       "* ощущают себя дезориентированным, потерянным;\n"
                       "* проявляют апатию, отсутствие интереса к чему-либо;\n"
                       "* замыкаются в себе, отказываются говорить о своих чувствах;\n"
                       "* испытывают высокую тревогу, плохо спят;\n"
                       "* отказываются принимать новое место жизни, требуют вернуть их домой;\n"
                       "* проявляют агрессию, устраивают протесты\n\n"
                       "Продолжительность - 8 встреч по 1.5 часа",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':10,
         'members':{},
         'queue':{}},
    'protest':
        {'name':"Группа \"Протест\"",
         'date_time':"по вторникам, 19:00 МСК",
         'reminder':"1_19:00",
         'specialist':"Александра Иванова",
         'picture':"NULL",
         'description':"История протестного движения в России последние лет 10 - это история людей, которые сказали \"я - против\" и оказались предателями своей своей страны. А о предателях не принято говорить.\n"
                       "Так нам предлагают думать властьимущие."
                       "И когда теми, кто принимает устрашающие людей законы, движет страх, людьми, выходящих на митинги, не боящихся сказать свое мнение, движет сила, совесть и невозможность молчать. "
                       "Так случилось, что эти качества не в почете. А говорить то, что думаешь, с каждым днём всё опаснее.\n\n"
                       "Человек, который столкнулся с непростым опытом, с насилием, может сломаться. Обычная жизнь \"после\" начинает подчиняться внутренним страхам в следствие пережитого опыта.\n\n"
                        "Возможно, Вы именно тот человек, который столкнулся с таким опытом. И наша группа будет для Вас тем безопасным пространством, где можно говорить обо всем. И, самое главное, о своей боли и страхах.\n\n"
                       "Для кого эта группа:\n"
                       "* Вы не понимаете, что с Вами происходит\n"
                       "* Вы боитесь обращаться за поддержкой и помощью\n"
                       "* Вы задаетесь вопросом \"что будет дальше?\" и не знаете ответ\n"
                       "* Вам знакома бессонница, потеря аппетита, кошмары\n"
                       "* человек в форме вызывает ужас и панику\n"
                       "* Вы чувствуете, что перестали справляться с простыми привычными  делами\n"
                       "* Вы не чувствуете себя в безопасности\n\n"
                       "Продолжительность -  8 встреч по 1,5 часа.",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':15,
         'members':{},
         'queue':{}},
    'movingout':
        {'name':"Группа для переезжающих/переехавших",
         'date_time':"по пятницам, 19:00 МСК",
         'reminder':"4_19:00",
         'specialist':"Александра Иванова",
         'picture':"NULL",
         'description':"Эмиграция относится к сильнейшим стоессам. Человеку приходится одновременно принимать потерю прежнего образа жизни  и усваивать нормы и правила новой стране.  И нередко вопросы \"кто я?\", \"Где мое место в мире?\", становятся актуальными, как никогда. Психическая нагрузка довольна сильная, эмоции становятся трудно выносимыми.\n\n"
                       "Мы открываем набор в группу для тех, кому трудно в этих непростых условиях. Эта группа для вас, если:\n\n"
                       "* вы планируете переезд\n"
                       "* вас не понимают близкие и/или вы испытываете чувство вины перед теми, кто остаётся\n"
                       "* вы переехали и вам трудно даются этапы адаптации\n"
                       "* вы не испытываете того ожидаемого чувства \"ну наконец-то!\"\n"
                       "* все текущие бытовые дела даются вам с трудом в новой стране\n"
                       "* вам трудно найти свой круг общения\n"
                       "* вы переехали и экстренно и до сих пор не понимаете, что происходит\n"
                       "* вы часто задаетесь вопросом \"правильно ли я поступил_а?\"\n"
                       "* вам сложно на новом месте по непонятным причинам\n"
                       "* свой вариант\n\n"
                       "Продолжительность - 8 встреч по 1,5 часа.",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':15,
         'members':{},
         'queue':{}},
    'stayinrussia':
        {'name':"Я остаюсь!",
         'date_time':"по вторникам, 19:00 МСК",
         'reminder':"1_19:00",
         'specialist':"Татьяна",
         'picture':"NULL",
         'description':"Группа для тех, кто принял для себя непростое решение остаться в России.\n\n"
                       "Те из нас, кто остался в России в эти непростые времена, сталкивается с определёнными трудностями. Здесь мы также встречаемся со страхом, неопределённостью, ощущением одиночества и разделённости. Поэтому сейчас каждому из нас как никогда нужна поддержка и чувство \"Я не один\".\n\n"
                       "Продолжительность - 5 недель.",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':10,
         'members':{},
         'queue':{}},
    'arttheraty':
        {'name':"Арт-терапия",
         'date_time':"по пятницам, 18:00 МСК",
         'reminder':"4_18:00",
         'specialist':"Надежда Балицкая",
         'picture':"NULL",
         'description':"Продолжительность - 8 недель.",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':10,
         'members':{},
         'queue':{}},
    'forparents':
        {'name':"Группа для родителей",
         'date_time':"по средам, 19:00 МСК",
         'reminder':"2_19:00",
         'specialist':"Дина Палеха",
         'picture':"NULL",
         'description':"\"Как сохранить себя, психику и отношения с детьми в условиях тотальной нестабильности\""
                       "Каждый день нам всем приходится принимать какие-то решения. Но если ты родитель, то эти решения - не только за себя.\n\n"
                       "* Как справиться с этим грузом ответственности и не провалиться в собственные детские страхи?\n"
                       "* Как разрешить себе - взрослому- проживание сложных чувств?]n"
                       "* Как научить ребёнка проживать свои?\n"
                       "* Как успокоить ребёнка, не впадая в собственную тревогу?\n"
                       "* Может ли родитель быть слабым?\n"
                       "* Как выстраивать диалог с близкими, не впадая в агрессию и не ранясь?\n"
                       "* Как говорить с детьми о важном и сложном?\n\n"
                       "Эти и другие вопросы мы разберём в закрытой группе для родителей. Группе для тех, кто каждый день принимает решения не только за себя. И сам при этом нуждается в эмоциональной поддержке.\n\n"
                       "Продолжительность - 5 недель",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':10,
         'members':{},
         'queue':{}},
    'blackbox':
        {'name':"Черный ящик",
         'date_time':"по пятницам, 20:30 МСК",
         'reminder':"4_20:30",
         'specialist':"",
         'picture':"NULL",
         'description':"Я есть и я здесь.\n\n"
                       "Продолжительность - 5 недель",
         'invite':f"Meeting ID: 230 365 3201 | Passcode: gaXp8U | <a href='https://us05web.zoom.us/j/2303653201?pwd=WWJ1a3ZoblVFWTJIRHh4cGt6K0ppdz09'>Zoom</a>",
         'opengroup':"0",
         'limit':15,
         'members':{},
         'queue':{}},
    'crisis':
        {'name':"Краткосрочная терапия",
         'date_time':"в удобное для Вас время по договоренности с терапевтом",
         'reminder':"",
         'specialist':"Терапевт-волонтер сообщества @helpwithoutprejudice",
         'picture':"NULL",
         'description':"Личная краткосрочная терапия для тех, кому срочно необходима поддержка",
         'invite':f"",
         'opengroup':"0",
         'limit':0,
         'members':{},
         'queue':{}}
}

admin_cids = ['5358195597']
user_cids = []

@bot.message_handler(commands=['lkjoiu'])
def start(m):
    user_cids.append(m.chat.id)
    # bot.send_message(chat_id="5358195597", text=f"Full user list: {set(user_cids)}", parse_mode='html')
    start_message = f"Здравствуйте! Это бот команды @helpwithoutprejudice. Мы оказываем психологическую поддержку всем, кому нелегко в нынешнее время.\n" \
                    f"С помощью этого бота Вы сможете посмотреть список групп психологической поддержки, создать напоминание, записаться в группу, отправить донат и запросить краткосрочную терапию с одним из наших терапевтов-волонтеров.\n" \
                    f"Вот список команд, которые понимает наш бот:\n /start - начать работу с ботом\n /help - посмотреть список команд\n /list - посмотреть список запланированных групп психологической помощи.\n"
    bot.send_message(m.chat.id, start_message, parse_mode='html', reply_markup=view_session_list())

@bot.message_handler(commands=['help'])
def help(m):
    help_message = f"Вот список команд, которые понимает наш бот:\n /start - начать работу с ботом\n /help - посмотреть список команд\n /list - посмотреть список запланированных групп психологической помощи.\n"
    # bot.send_message(m.chat.id, m.chat, parse_mode='html')
    bot.send_message(m.chat.id, help_message, parse_mode='html')

@bot.message_handler(commands=['list'])
def list(m):
    session_list_message = f"Список групп психологической помощи:"
    # bot.send_message(m.chat.id, m.chat, parse_mode='html')
    bot.send_message(m.chat.id, session_list_message, parse_mode='html', reply_markup=session_list())

@bot.message_handler(commands=['whoami'])
def who_am_i(m):
    if (m.chat.id in admin_cids):
        telegram_data = f"{m.chat}"
        bot.send_message(m.chat.id, telegram_data, parse_mode='html')

@bot.message_handler(commands=['getall'])
def who_am_i(m):
    if (m.chat.id in admin_cids):
        for key in session_list_dic.keys():
            bot.send_message(m.chat.id, session_list_dic[key], parse_mode='html')

@bot.message_handler(commands=['admin'])
def admin(m):
    if str(m.chat.id) in admin_cids:
        bot.send_message(m.chat.id, "Commands:", reply_markup=admin_commands())

@bot.message_handler()
def sample_message(m):
    global session_list_dic
    cid = m.chat.id
    if (cid in session_list_dic['crisis']['members'].keys()):
        del session_list_dic['crisis']['members'][cid]
        crisis_to_volunteer(m)
        bot.send_message(m.chat.id, "Спасибо. Наш терапевт свяжется с Вами.", reply_markup=view_session_list())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global session_list_dic
    if call.data in set(session_list_dic.keys()):
        bot.answer_callback_query(call.id, "")
        session_item = session_list_dic[call.data]
        session_info = f"<b>{session_item['name']}</b>\n\n<b>Время</b>: {str(session_item['date_time'])}\n<b>Ведущий терапевт</b>: {session_item['specialist']}\n<b>Аннотация</b>:\n{session_item['description']}"
        if (session_item['picture'] != "NULL"):
            photo = open(session_item['picture'], 'rb')
            bot.send_photo(call.message.chat.id, photo)
        label = str(call.data)+'_'+str(call.message.chat.id)

        if call.data == "crisis":
            # session_list_dic['crisis']['members'].append(call.message.chat.id)
            session_list_dic['crisis']['members'][call.message.chat.id] = {'chat_id':call.message.chat.id,'first_name':call.message.chat.first_name,'last_name':call.message.chat.last_name,'user_name':call.message.chat.username}
            bot.send_message(call.message.chat.id, "Опишите свою проблему в одном сообщении. Это поможет нам подобрать терапевта для Вас.", parse_mode='html')

        elif(session_item['opengroup'] == "1"):
            session_info = session_info + f"\n\n<b>Ссылка для подключения:</b>\n{session_item['invite']}"
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())

        elif((session_item['opengroup'] == "2") & (session_item['limit'] > 0) & (not call.message.chat.id in session_item['members'].keys())):
            session_info = session_info + f"\n\n<b>Ссылка для подключения:</b>\n{session_item['invite']}"
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())
            session_list_dic[call.data]['members'][call.message.chat.id] = {'first_name':call.message.chat.first_name,'last_name':call.message.chat.last_name,'user_name':call.message.chat.username}
            session_list_dic[call.data]['limit'] -= 1

        elif((session_item['opengroup'] == "2") & (session_item['limit'] <= 0) & (not call.message.chat.id in session_item['members'].keys())):
            session_info = session_info + f"\n\nК сожалению, набор в это группу закрыт. Если в группе появятся места - мы пришлем уведомление."
            session_list_dic[call.data]['queue'][call.message.chat.id] = {'first_name':call.message.chat.first_name,'last_name':call.message.chat.last_name,'user_name':call.message.chat.username}
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())

        elif((session_item['opengroup'] == "2") & (call.message.chat.id in session_item['members'].keys())):
            session_info = f"Вы уже записаны в эту группу. Будем ждать Вас {session_item['date_time']}.\n\nСсылка для подключения: {session_item['invite']}"
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())

        elif ((session_item['opengroup'] == "0") & (session_item['limit'] > 0) & (not call.message.chat.id in session_item['members'].keys())):
            session_info = session_info + f"\n\nЭто <b>закрытая группа</b> с ограниченым количеством участников (осталось <b>{session_item['limit']}</b> мест). Записаться можно отправив любую предложенную сумму в качестве пожертвования.\n\n" \
                                          f"<b>Инструкция:</b>\n" \
                                          f"* нажмите на кнопку с суммой, которую хотите пожертвовать, и перейдите по ссылке\n" \
                                          f"* пожертвование можно внести с помощью карты или ЯндексКошелька\n" \
                                          f"* <b>важно:</b> после успешного перевода вернитесь в чат бота и нажмите кнопку <b>Подтвердить</b>. Так мы сможем отследить Ваш донат и прислать ссылку для подключения. Обычно это занимает несколько минут\n" \
                                          f"* если все прошло хорошо, Вы автоматически получите ссылку для подключения через бот. Если Вы не получили ссылку или получили сообщение об ошибке, свяжитесь с @kolin_drafter, мы проверим перевод вручную."
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=donate(label, True))
            # bot.send_photo(call.message.chat.id, photo, reply_markup=donate(label))

        elif ((session_item['opengroup'] == "0") & (call.message.chat.id in session_item['members'].keys())):
            session_info = f"Вы уже записаны в эту группу. Будем ждать Вас {session_item['date_time']}.\n\nСсылка для подключения: {session_item['invite']}"
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())

        elif ((session_item['opengroup'] == "0") & (session_item['limit'] <= 0)):
            session_info = session_info + f"\n\nК сожалению, набор в это группу закрыт. Если в группе появятся места - мы пришлем уведомление."
            session_list_dic[call.data]['queue'][call.message.chat.id] = {'first_name':call.message.chat.first_name,'last_name':call.message.chat.last_name,'user_name':call.message.chat.username}
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())
        else:
            session_info = session_info + f"Хм... Что-то пошло не так...\n" \
                                          f"Попробуйте еще раз или поищите информацию в @helpwithoutprejudice. Там мы публикуем анонсы всех мероприятий."
            bot.send_message(call.message.chat.id, session_info, parse_mode='html', reply_markup=view_session_list())

    elif call.data == "just_donation":
        bot.answer_callback_query(call.id, "")
        label = 'justdonate'+'_'+str(call.message.chat.id)
        thank_you_message = f"Вы решили поддержать наш проект. Мы благодарны Вам. Выберите сумму, которую Вы хотели бы пожертвовать:"
        bot.send_message(call.message.chat.id, thank_you_message, parse_mode='html', reply_markup=donate(label, False))

    elif bool(re.match('^checkdonate',call.data)):
        label = call.data.replace('checkdonate_',"")
        checkdonate_list = label.split('_')
        session_item = session_list_dic[checkdonate_list[0]]
        if (not call.message.chat.id in session_item['members'].keys()):
            bot.answer_callback_query(call.id, "")
            session_list_dic[checkdonate_list[0]]['members'][call.message.chat.id] = {'first_name':call.message.chat.first_name,'last_name':call.message.chat.last_name,'user_name':call.message.chat.username}
            # bot.answer_callback_query(call.id, "")
            successful_donate_message = f"Мы получили Ваше пожертвование! Спасибо!\n\nСсылка для подключения к закрытой конференции:\n {session_item['invite']}\n\nБудем ждать Вас {session_item['date_time']}"
            message_to_admin = f"Пришел донат на запись в группу {session_item['name']}.\nОтправитель: {call.message.chat.first_name} {call.message.chat.last_name}, @{call.message.chat.username}\nИдентификатор платежа: {label}"
            # Timer(1,check_payment_status(call.message.chat.id, label, successful_donate_message, message_to_admin)).start()

            a_thread = threading.Thread(check_payment_status(call.message.chat.id, label, successful_donate_message, message_to_admin, session_item['reminder']))
            a_thread.start()
            a_thread.join()
        else:
            bot.answer_callback_query(call.id, f"Вы уже записаны в эту группу. Будем ждать Вас {session_item['date_time']}.\n\nСсылка для подключения: {session_item['invite']}")

    elif ((str(call.message.chat.id) in admin_cids) & (call.data == "review_group")):
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "Choose group", reply_markup=view_group_info('review_group'))

    elif ((str(call.message.chat.id) in admin_cids) & (bool(re.match('^review_group',call.data)))):
        bot.answer_callback_query(call.id, "")
        session_item = session_list_dic[call.data.split('_')[-1]]
        message_for_admin = ""
        for key in session_item.keys():
            message_for_admin = message_for_admin + f"<b>{key}:</b> {session_item[key]}\n"
        bot.send_message(call.message.chat.id, message_for_admin, parse_mode='html', reply_markup=admin_commands())

    elif ((str(call.message.chat.id) in admin_cids) & (call.data == "set_limit")):
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "Choose group", reply_markup=view_group_info('set_limit'))

    elif ((str(call.message.chat.id) in admin_cids) & (bool(re.match('^set_limit',call.data)))):
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "New limit", reply_markup=set_new_limit(call.data))

    elif ((str(call.message.chat.id) in admin_cids) & (bool(re.match('^set_new_limit',call.data)))):
        bot.answer_callback_query(call.id, "")
        label = call.data.split('_')
        session_item = session_list_dic[label[-2]]
        if (int(label[-1]) > session_item['limit']):
            for cid in session_item['queue'].keys():
                bot.send_message(chat_id=cid, text=f"Появились новые места в группу \"{session_item['name']}\". Вы получили это сообщение, т.к. пытались записаться ранее. Чтобы попасть в группу, нажмите на кнопку ниже, выберите группу \"{session_item['name']}\", а затем \"Записаться\". Места могут быстро закончиться, если в очереди много участников.", parse_mode='html', reply_markup=view_session_list())
            session_list_dic[label[-2]]['queue'] = {}

        session_list_dic[label[-2]]['limit'] = int(label[-1])
        session_item = session_list_dic[label[-2]]
        message_for_admin = ""
        for key in session_item:
            message_for_admin = message_for_admin + f"<b>{key}:</b> {session_item[key]}\n"
        for cid in admin_cids:
            bot.send_message(cid, message_for_admin, parse_mode='html', reply_markup=admin_commands())

    elif ((str(call.message.chat.id) in admin_cids) & (call.data == "create_reminder")):
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "Choose group", reply_markup=view_group_info('create_reminder'))

    elif ((str(call.message.chat.id) in admin_cids) & (bool(re.match('^create_reminder',call.data)))):
        bot.answer_callback_query(call.id, "")
        label = call.data.split('_')
        session_item = session_list_dic[label[-1]]

        if (session_item['reminder'] != ""):
            next_session = session_item['reminder'].split('_')
            next_seven_days = [datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(days=x) for x in range(7)]
            reminder_date = [x for x in next_seven_days if str(x.weekday()) == next_session[0]][0]
            next_session = datetime.strptime(next_session[-1],"%H:%M")
            reminder_date = reminder_date.replace(hour=next_session.hour, minute=next_session.minute)

            time_diff = int((reminder_date - datetime.now(pytz.timezone('Europe/Moscow'))).total_seconds() / 60.0)

            for cid in session_item['members'].keys():
                bot.send_message(cid, f"<b>{session_item['name']}:</b> встречаемся через {time_diff} минут.\n\nСсылка для подключения:\n{session_item['invite']}", parse_mode='html', reply_markup=view_session_list())

    elif ((str(call.message.chat.id) in admin_cids) & (call.data == "remove_member")):
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "Choose group", reply_markup=view_group_info('rm_group'))

    elif ((str(call.message.chat.id) in admin_cids) & (bool(re.match('^rm_group',call.data)))):
        bot.answer_callback_query(call.id, "")
        session_item = session_list_dic[call.data.split('_')[-1]]['members']
        bot.send_message(call.message.chat.id, "Choose member", reply_markup=remove_member(call.data, session_item))

    elif ((str(call.message.chat.id) in admin_cids) & (bool(re.match('^rm_member',call.data)))):
        bot.answer_callback_query(call.id, "")
        del session_list_dic[call.data.split('_')[-2]]['members'][int(call.data.split('_')[-1])]
        session_list_dic[call.data.split('_')[-2]]['limit'] += 1
        bot.send_message(call.message.chat.id, "Member removed", reply_markup=admin_commands())

    elif call.data == "session_list":
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "Список групп поддержки в сообществе:", reply_markup=session_list())

    else:
        bot.answer_callback_query(call.id, "")
        bot.send_message(call.message.chat.id, "Нажмите \"Посмотреть\", чтобы открыть список групп поддержки в сообществе.", reply_markup=view_session_list())

def admin_commands():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Review groups",callback_data="review_group"),
               InlineKeyboardButton("Change group limit",callback_data="set_limit"),
               InlineKeyboardButton("Create reminder",callback_data="create_reminder"),
               InlineKeyboardButton("Remove member",callback_data="remove_member"))
    return markup

def crisis_to_volunteer(who):
    for v in admin_cids:
        bot.send_message(chat_id=v,
                         text=f"У нас есть заявка на кризисную терапию.\n"
                              f"От: {who.chat.first_name} {who.chat.last_name} @{who.chat.username}\n"
                              f"Запрос: {who.text}")

def view_session_list():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Посмотреть список групп", callback_data="session_list"))
    return markup

def view_group_info(label):
    global session_list_dic
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for key in session_list_dic.keys():
        markup.add(InlineKeyboardButton(session_list_dic[key]['name'], callback_data=label+"_"+key))
    return markup

def remove_member(label, session_list):
    label = label.replace("group","member")
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for key in session_list.keys():
        markup.add(InlineKeyboardButton(f"{session_list[key]['first_name']} {session_list[key]['last_name']} {session_list[key]['user_name']}", callback_data=label+"_"+str(key)))
    return markup

def set_new_limit(label):
    label = label.replace("set_limit","set_new_limit")
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(
        InlineKeyboardButton("1", callback_data=label+"_"+"1"),
        InlineKeyboardButton("2", callback_data=label+"_"+"2"),
        InlineKeyboardButton("3", callback_data=label+"_"+"3"),
        InlineKeyboardButton("4", callback_data=label+"_"+"4"),
        InlineKeyboardButton("5", callback_data=label+"_"+"5"),
        InlineKeyboardButton("6", callback_data=label+"_"+"6"),
        InlineKeyboardButton("7", callback_data=label+"_"+"7"),
        InlineKeyboardButton("8", callback_data=label+"_"+"8"),
        InlineKeyboardButton("9", callback_data=label+"_"+"9"),
        InlineKeyboardButton("10", callback_data=label+"_"+"10"),
        InlineKeyboardButton("11", callback_data=label+"_"+"11"),
        InlineKeyboardButton("12", callback_data=label+"_"+"12"),
        InlineKeyboardButton("13", callback_data=label+"_"+"13"),
        InlineKeyboardButton("14", callback_data=label+"_"+"14"),
        InlineKeyboardButton("15", callback_data=label+"_"+"15"),
        InlineKeyboardButton("16", callback_data=label+"_"+"16"),
        InlineKeyboardButton("17", callback_data=label+"_"+"17"),
        InlineKeyboardButton("18", callback_data=label+"_"+"18"),
        InlineKeyboardButton("19", callback_data=label+"_"+"19"),
        InlineKeyboardButton("20", callback_data=label+"_"+"20"))
    return markup

def session_list():
    global session_list_dic
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for key in session_list_dic.keys():
        markup.add(InlineKeyboardButton(session_list_dic[key]['name'], callback_data=key))
    markup.add(InlineKeyboardButton("Пожертвование", callback_data="just_donation"))
    return markup

def check_payment_status(to, label, successful_donate_message, message_to_admin, check_date):
#     5358195597
    global session_list_dic
    payment_status = False
    checkdonate_list = label.split('_')
    dt_start = datetime.now()

    utc=pytz.UTC
    next_session = check_date.split('_')
    next_seven_days = [datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(days=x) for x in range(7)]
    reminder_date = [x for x in next_seven_days if str(x.weekday()) == next_session[0]][0]
    next_session = datetime.strptime(next_session[-1],"%H:%M")
    reminder_date = reminder_date.replace(hour=next_session.hour, minute=next_session.minute, tzinfo=utc) - timedelta(days=7)

    while(not payment_status):
        history = client.operation_history(label=label)
        operations = [x for x in history.operations if utc.localize(x.datetime) > reminder_date]
        # operations = history.operations
        for operation in operations:
            if (operation.status == "success"):
                bot.send_message(to, successful_donate_message, parse_mode='html', reply_markup=view_session_list())
                payment_status = True
            else:
                time.sleep(10)
        if ((datetime.now()-dt_start).total_seconds() > 300):
            while (int(checkdonate_list[1]) in session_list_dic[checkdonate_list[0]]['members'].keys()):
                del session_list_dic[checkdonate_list[0]]['members'][int(checkdonate_list[1])]
            bot.send_message(to, f"Мы не смогли подтвердить Ваш платеж. Если Вы считаете, что произошла ошибка - свяжитесь с @kolin_drafter", parse_mode='html', reply_markup=view_session_list())
            break

    if(payment_status):
        session_list_dic[checkdonate_list[0]]['limit'] -= 1
        for cid in admin_cids:
            bot.send_message(chat_id=cid, text=message_to_admin+f"\nВремя платежа: {operation.datetime}\nВ группе осталось <b>{session_list_dic[checkdonate_list[0]]['limit']}</b> мест.", parse_mode='html')

def donate(label, confirmation):
    RUR_100 = Quickpay(
            receiver="4100117805460248",
            quickpay_form="donate",
            targets="Sponsor this project",
            paymentType="SB",
            sum=10,
            label=label)

    RUR_500 = Quickpay(
            receiver="4100117805460248",
            quickpay_form="donate",
            targets="Sponsor this project",
            paymentType="SB",
            sum=500,
            label=label)

    RUR_1000 = Quickpay(
            receiver="4100117805460248",
            quickpay_form="donate",
            targets="Sponsor this project",
            paymentType="SB",
            sum=1000,
            label=label)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("RUR 100", url=RUR_100.redirected_url, callback_data="rur_100"),
               InlineKeyboardButton("RUR 500", url=RUR_500.redirected_url, callback_data="rur_500"),
               InlineKeyboardButton("RUR 1000", url=RUR_1000.redirected_url, callback_data="rur_1000"))
    if (confirmation):
        markup.add(InlineKeyboardButton("Подтвердить", callback_data="checkdonate_"+label),
               InlineKeyboardButton("Вернуться к списку групп", callback_data="session_list"))
    else:
        markup.add(InlineKeyboardButton("Вернуться к списку групп", callback_data="session_list"))
    return markup

bot.polling(none_stop=True, interval=5)
# bot.infinity_polling(True)
# bot.infinity_polling(timeout=10, long_polling_timeout = 5)

# globals().clear()