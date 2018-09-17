from answers import opinions
import telebot
import json
import time
import logging

with open('config.json') as json_data:
    token = json.load(json_data)
bot = telebot.TeleBot(token['token'])


class User:
    def __init__(self, id):
        self.id = id
        self.status = None
        self.potential_partner_id = None
        self.partner_id = None
        self.opinion = None
        self.just_begin = True
        self.mode = None
        self.pagination = 0
        self.answer_2 = None

    def _change_status(self, status):
        self.status = status

    def _set_potential_partner(self, potential_partner_id):
        self.potential_partner_id = potential_partner_id

    def _connect_partner(self, partner_id):
        self.partner_id = partner_id

    def _change_opinion(self, opinion):
        self.opinion = opinion

    def _change_pagination(self, page):
        self.pagination = page

    def _set_mode(self, mode):
        self.mode = mode

    def _set_answer_2(self, answer):
        for i in range(1, opinions[self.opinion]['description']['len']+1):
            if answer in opinions[self.opinion]['description'][i]:
                self.answer_2 = i
                break


users = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(
        message.from_user.id,
        'Добро пожаловать. \n'
        'Чтобы *определить* Ваше настроение, состояние и потребности, используйте команду /test \n'
        'Больше команд /help',
        parse_mode='Markdown',
    )


@bot.message_handler(commands=['stop'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(
        message.from_user.id,
        'Вы прекратили прохождение теста. Напишите /test чтобы начать его заново',
        reply_markup=user_markup
    )
    try:
        users[message.from_user.id]._change_status(0)
    except:
        logging.info(f'Sent /stop + added new user {message.from_user.id}')
        user = User(message.from_user.id)
        user._change_status(0)
        users[message.from_user.id] = user


@bot.message_handler(commands=['id'])
def handle_start(message):
    bot.send_message(message.from_user.id, 'Твой id : ' + str(message.from_user.id) + '\nСкопируй его, чтобы '
                                                                                      'отправить партнёру.')


@bot.message_handler(commands=["help"])
def handle_text(message):
    bot.send_message(
        message.chat.id,
        """
        Есть набор следующий команд:
        /test - начать тест
        /id - получить свой id (нужен, чтобы отправить партнёру для старта теста)
        /start - приветственное сообщение
        /stop - закрыть клавиатуру/прервать прохождение теста
        /help - узнать список команд
        """,
    )


@bot.message_handler(commands=["test"])
def handle_text(message):
    logging.info(str(users.keys()))
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('соло')
    user_markup.row('в паре')
    bot.send_message(message.from_user.id, 'Пройти в соло или в паре?', reply_markup=user_markup)
    return


@bot.message_handler(content_types='text')
def handle_text(message):
    if message.text == 'в паре':
        if message.from_user.id not in users:
            user = User(message.from_user.id)
            users[message.from_user.id] = user
        users[message.from_user.id]._change_status(0)
        users[message.from_user.id]._set_mode('в паре')
        bot.send_message(
            message.from_user.id,
            'Пусть ваш парнёт наберёт кодовую фразу: ')
        bot.send_message(
            message.from_user.id,
            'Коннект: ' + str(message.from_user.id))
        return

    elif message.text == 'соло':
        if message.from_user.id not in users:
            user = User(message.from_user.id)
            users[message.from_user.id] = user
        users[message.from_user.id]._change_status(1)
        users[message.from_user.id]._set_mode('соло')
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('клево')
        user_markup.row('не очень')
        bot.send_message(message.from_user.id, 'Как настроение?', reply_markup=user_markup)
        return

    try:
        if message.text.split(':')[0].lower() == 'коннект':
            bot.send_message(message.text.split(':')[1].strip(), f'Вы уверены, что хотите приконнектиться к '
                                                                 f'{message.from_user.id}? Если да, напи'
                                                                 'шите "Коннект подтвержден"')
            partner_id = int(message.text.split(':')[1].strip())
            if partner_id not in users:
                user = User(partner_id)
                users[partner_id] = user
            if message.from_user.id not in users:
                user = User(message.from_user.id)
                users[message.from_user.id] = user
            users[partner_id]._set_potential_partner(message.from_user.id)
            users[message.from_user.id]._set_potential_partner(partner_id)
            # return
    except Exception as e:
        logging.info(e.args)
        logging.info('Incorrect <id>')
        print('Incorrect <id>', end='\r')

    if 'коннект подтвержден' in message.text.lower().replace('ё', 'е'):
        print(users)
        print(users[message.from_user.id])
        print(users[message.from_user.id].potential_partner_id)
        our_partner_id = users[message.from_user.id].potential_partner_id
        print(f'Our: {our_partner_id}')
        users[our_partner_id]._connect_partner(message.from_user.id)
        users[message.from_user.id]._connect_partner(our_partner_id)
        bot.send_message(message.from_user.id, 'Успешно')
        bot.send_message(our_partner_id, 'Успешно')
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Клево')
        user_markup.row('Не очень')
        bot.send_message(message.from_user.id, 'Как настроение?', reply_markup=user_markup)
        users[message.from_user.id]._change_status(1)
        bot.send_message(our_partner_id, 'Как настроение?', reply_markup=user_markup)
        users[our_partner_id]._change_status(1)
        return

    try:
        opinion = users[message.from_user.id].opinion
        status = users.get(message.from_user.id).status
        if status == 1:
            if message.text.lower() == 'клево':
                users[message.from_user.id]._change_opinion('клево')
            elif message.text.lower() == 'не очень':
                users[message.from_user.id]._change_opinion('не очень')
            users[message.from_user.id]._change_status(2)
            users[message.from_user.id].just_begin = True
        opinion = users[message.from_user.id].opinion
        status = users.get(message.from_user.id).status

        if status == 2:
            if message.text.lower() == 'другое' or users[message.from_user.id].just_begin:
                if users[message.from_user.id].pagination > 6:
                    users[message.from_user.id]._change_pagination(0)
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                for i in range(1, opinions[opinion]['description']['len']+1):
                    user_markup.row(
                        opinions[opinion]['description'][i][users[message.from_user.id].pagination]
                    )
                if users[message.from_user.id].just_begin:
                    bot.send_message(message.from_user.id, text=f'{opinion.capitalize()} это как?', reply_markup=user_markup)
                else:
                    bot.send_message(message.from_user.id, text='..', reply_markup=user_markup)
                users[message.from_user.id].just_begin = False
                users[message.from_user.id].pagination += 1
            else:
                users[message.from_user.id]._set_answer_2(message.text.lower())
                users[message.from_user.id]._change_status(3)
                users[message.from_user.id]._change_pagination(0)
                users[message.from_user.id].just_begin = True
        status = users.get(message.from_user.id).status
        if status == 3:
            if message.text.lower() == 'другое' or users[message.from_user.id].just_begin:
                if users[message.from_user.id].pagination > 13:
                    users[message.from_user.id]._change_pagination(0)
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                for i in range(1, 5):
                    user_markup.row(opinions[opinion]['state_is'][i][users[message.from_user.id].pagination])
                if users[message.from_user.id].just_begin:
                    if opinion == 'клево':
                        bot.send_message(
                            message.from_user.id,
                            text=f'{message.text.capitalize()} там где есть ... ',
                            reply_markup=user_markup
                        )
                    else:
                        bot.send_message(
                            message.from_user.id,
                            text='Что могло бы сейчас тебе поднять настроение?',
                            reply_markup=user_markup
                        )
                else:
                    bot.send_message(message.from_user.id, '..', reply_markup=user_markup)
                users[message.from_user.id].pagination += 1
                users[message.from_user.id].just_begin = False
            else:
                users[message.from_user.id]._change_status(4)
        status = users.get(message.from_user.id).status
        if status == 4:
            msg = message.text.lower()
            ans = 1
            for i in range(1, 4):
                if msg in opinions[opinion]['state_is'][i]:
                    ans = i
                    break
            user_markup = telebot.types.ReplyKeyboardRemove()
            bot.send_message(
                message.from_user.id,
                f'Для тебя важно иметь {msg}, потому что сейчас на самом деле ты хочешь '
                f'{opinions[opinion]["wants"][ans]}.',
                reply_markup=user_markup
            )
            if opinion == 'не очень':
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                user_markup.row('завершить тест')
                user_markup.row('совет для себя')
                user_markup.row('совет для партнёра')
                bot.send_message(
                    message.from_user.id,
                    'Вы прошли тест и мы можем дать совет по полученным результатам',
                    reply_markup=user_markup
                )
                users[message.from_user.id]._change_status(5)
                return
            else:
                bot.send_message(
                    message.from_user.id,
                    'Продолжайте в том же духе. Вы отлично справляетсь и не нуждаетесь в дополнительных советах. '
                )
                bot.send_message(
                    message.from_user.id,
                    'Ты можешь пройти опрос для сбора статистики. Сделай это пожалуйста., '
                    'https://docs.google.com/forms/d/1UNZBQ0V5uSe5S5FesYiCq4og4tuWA_sItVdd2g-wdkM/edit',
                )
                users[message.from_user.id]._change_status(0)
                return

        status = users.get(message.from_user.id).status
        if status == 5:
            if opinion == 'не очень':
                users[message.from_user.id]._change_status(0)
                if message.text.lower() == 'завершить тест':
                    bot.send_message(
                        message.from_user.id,
                        'Ты можешь пройти опрос для сбора статистики. Сделай это пожалуйста., '
                        'https://docs.google.com/forms/d/1UNZBQ0V5uSe5S5FesYiCq4og4tuWA_sItVdd2g-wdkM/edit',
                    )

                if message.text.lower() == 'совет для себя':
                    bot.send_message(
                        message.from_user.id,
                        opinions[opinion]['my_advices'][users[message.from_user.id].answer_2]
                    )
                if message.text.lower() == 'совет для партнёра':
                    while True:
                        if users[users[message.from_user.id].partner_id].status == 0:
                            bot.send_message(
                                users[message.from_user.id].partner_id,
                                opinions[opinion]['partner_advices'][users[message.from_user.id].answer_2]
                            )
                            break
                        time.sleep(1)
    except Exception as e:
        logging.info(e.args)


def main():
    logging.basicConfig(filename='errors.log', level=logging.INFO)
    logging.info('START')
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.info(e.args)
        logging.info('FINISH')
        raise e
    # while True:
    #     try:
    #         bot.polling(none_stop=True)
    #     except Exception as e:
    #         logging.info(e.args)
    #         time.sleep(5)
    #         logging.info('ReSTART 5s')


if __name__ == '__main__':
    main()
