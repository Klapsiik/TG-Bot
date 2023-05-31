from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import CommandHandler, ConversationHandler
from key import TOKEN


from base import get_user_from_db, write_to_db  # TODO не видит get_user_from_db из-за того, что закомментировала
                                                # TODO текст в ask_class (User) - 88 строчка


GRADES = (
    '8н', '8о', '8п',
    '9н', '9о', '9п',
    '10н', '11н', '11о',
)

WAIT_FOR_CLASS, WAIT_FOR_NAME, WAIT_FOR_PHOTO = range(3)

def main():
    """
    конфигуррирует и запускает бот
    """
    # Updater - объект, который ловит обновление из Телеграмма
    updater = Updater(token=TOKEN)

    # Диспетчер будет рапределять события по обработчикам
    dispatcher = updater.dispatcher

    # Добавляем обработчик события из Телеграмма
    dispatcher.add_handler(CommandHandler('start', do_start))
    dispatcher.add_handler(CommandHandler('ask_name', ask_name))
    dispatcher.add_handler(CommandHandler('ask_class', ask_class))
    dispatcher.add_handler(CommandHandler('ask_photo', ask_photo))
    dispatcher.add_handler(CommandHandler('register_player', register_player))

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('register', ask_class)],  # Точки старта диалого
            states={
                WAIT_FOR_CLASS: [CallbackQueryHandler(inline_reaction)],
                WAIT_FOR_NAME: [MessageHandler(Filters.text, get_name)],
                WAIT_FOR_PHOTO: [MessageHandler(Filters.text, get_photo)],
            },  # Состояние
            fallbacks=[]  # Отлов ошибок
        )
    )
    # TODO предупреждает об ошибке:
    """
    UserWarning: If 'per_message=False', 'CallbackQueryHandler' 
    #  will not be tracked for every message.warnings.warn(
    """
    # TODO предполагаю из-за команд в строках 38 и 40

    dispatcher.add_handler(MessageHandler(Filters.text, do_help))
    dispatcher.add_handler(
    CallbackQueryHandler(inline_reaction)
    )

    # Начать бесконечный опрос Телеграмма на предмет обновлений
    updater.start_polling()
    print(updater.bot.getMe())
    print('Бот запущен')
    updater.idle()

def do_help(update, context: CallbackContext): # запускаем бота
    text = [
        'Привет!',
        'Нажми на /register',
    ]
    text = '\n'.join(text)
    update.message.reply_text(text)


def register(update, context: CallbackContext):
    return ask_class(update, context)

def do_start(update, context: CallbackContext): # запускаем бота
    text = [
        'Привет!',
        'Я помогу тебе принять участие в игре "Killer"',
        'Для этого нажми на /register',
    ]
    text = '\n'.join(text)  # Собираем строки в текст через разделитель
    update.message.reply_text(text)


def ask_class(update, context: CallbackContext): # запускаем бота
    # user = get_user_from_db(update.message.from_user.id)
    # if user:
    #     lines = [
    #         f'Ты уже зарегистрирован под именем {user["name"]}',
    #         f'в классе {user["query.data"]}',
    #     ]
    #
    #     text = '\n'.join(lines)
    #     update.message.reply_text(text)
    #
    #     return ConversationHandler.END
    # TODO закомментировала потому-что выдавал ошибку:
    """
     File "D:\ШКОЛА\папка\02 Информатика\TG bot\base.py", line 30, in get_user_from_db
        user_id, query, name, photo = line.strip().split('\t')
ValueError: too many values to unpack(expected 4)
"""
    # TODO её решить у меня не получилось

    buttons = [
        [InlineKeyboardButton('8н', callback_data='8н'),
        InlineKeyboardButton('8о', callback_data='8о'),
        InlineKeyboardButton('8п', callback_data='8п')],
        [
        InlineKeyboardButton('9н', callback_data='9н'),
        InlineKeyboardButton('9о', callback_data='9о'),
        InlineKeyboardButton('9п', callback_data='9п')],
        [
        InlineKeyboardButton('10н', callback_data='10н'),
        InlineKeyboardButton('11н', callback_data='11н'),
        InlineKeyboardButton('11о', callback_data='110')],
    ]

    keyboard = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Выбери свой класс:'
    update.message.reply_text(text, reply_markup=keyboard)

    return WAIT_FOR_CLASS


def inline_reaction(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # TODO - запомнить класс в базу данных
    # query = context.args
    # context.user_data['query.data'] = query
    # grade = context.args
    # grade = update.callback_query
    # context.user_data['grade'] = grade
    # query.data = update.callback_query['query']
    context.user_data["query.data"] = query
    # TODO из всех вышеперечисленных вариантов, предположила этот

    return ask_name(update, context)


def ask_name(update: Update, context: CallbackContext): # запускаем бота
    query = update.callback_query
    text = [
        f'Я запомнил твой класс {query.data}',
        'Введите своё имя:'
    ]
    text = '\n'.join(text)
    query.edit_message_text(text)

    return WAIT_FOR_NAME


def get_name(update: Update, context: CallbackContext): # запускаем бот
    name = update.message.text
    context.user_data['name'] = name
    text = f'Я запомнил Ваше имя - {name}'
    update.message.reply_text(text)

    return ask_photo(update, context)


def ask_photo(update: Update, context: CallbackContext): # запускаем бота
    text = 'Прикрепи своё фото'
    update.message.reply_text(text)

    return WAIT_FOR_PHOTO


def get_photo(update: Update, context: CallbackContext): # запускаем бота
    photo = update.message.text
    context.user_data['photo'] = photo
    text = f'Я загрузил ваше фото: {photo}'
    update.message.reply_text(text)
 
    return register_player(update, context)


def register_player(update: Update, context: CallbackContext): # запускаем бота
    user_id = update.message.from_user.id
    query = context.user_data["query.data"]
    name = context.user_data["name"]
    photo = context.user_data["photo"]

    # TODO из-за переменной query выдаёт ошибку
    # TODO изначально вот такую:
    """
    typeerror: write() argument must be str, not callbackquery
    """
    # TODO после того как в папке "base" исправила 15 строчку, появилась другая ошибка:
    """
    File "D:\ШКОЛА\ папка\02 Информатика\01 python\lib\encodings\cp1251.py", line 19, in encode
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]
UnicodeEncodeError: 'charmap' codec can't encode character '\u2728' in position 562: character maps to <undefined>
"""
    # TODO её не разобрала. Видимо проблема в кодировке и переменную "query" нельзя присвоить и к
    # TODO "CallbackQuery" и к "str"

    # TODO в итоге с запоминанием информации вышли проблемы ((

    write_to_db(user_id, query, name, photo)

    lines = ['Ты зарегистрирован!',
             f'Ты учишься в классе {query.data}',
             f'Тебя зовут{name}']
    text = '\n'.join(lines)
    update.message.reply_text(text)

    return ConversationHandler.END



if __name__ == '__main__':
    main()