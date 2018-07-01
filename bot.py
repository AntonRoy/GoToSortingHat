import telebot
from telebot import types
bot = telebot.TeleBot("619811489:AAGJaJly2RWEFqld6ar4vt1cp6gplgxjDbI")
not_done = {}
no_name_answer = "You haven't sent me his/her name. Send it, please:"


@bot.message_handler(commands=['start', 'help'])
def reply_to_start(message):
    bot.send_message(message.chat.id, "Welcome to Sorting Hat! This bot will help you to distribute students in "
                                      "different courses. To get information, send the photo of a student and write his name in "
                                      "a caption.")


@bot.message_handler()
def reply_to_text(message):
    if message.reply_to_message != None and message.reply_to_message.text == no_name_answer:
        print('name =', message.text, 'filepath =', not_done[message.chat.id])
        del not_done[message.chat.id]
        bot.send_message(message.chat.id, "Thank you!")
    else:
        bot.reply_to(message, "I don't understand you. Type /help to get introduction")


@bot.message_handler(content_types=["photo"])
def get_photo(message):

    file_id = message.photo[2].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f'photos/{file_id}.jpg'

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    if message.caption != None:
        print('name =', message.caption, 'filepath =', file_path)
        bot.reply_to(message, "Thanks!")
    else:
        not_done[message.chat.id] = file_path
        markup = types.ForceReply(selective=True)
        bot.send_message(message.chat.id, no_name_answer, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)