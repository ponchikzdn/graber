from pyrogram import Client, filters
from datetime import datetime
import config
from sql import SQL


app = Client('bot_python', config.api_id, config.api_hash)
bd = SQL('bd.db')


@app.on_message(filters.chat(bd.get_donor()))
def get_post(client, message):
    username = message.chat.username
    message_id = message.message_id

    if not bd.message_id_exists(username, message_id):
        bd.add_message_id(username, message_id)
        # получение последнего ROWID
        for a in bd.get_last_rowid():
            last_id = a[0]

        # перессылка поста на модерку
        message.forward(bd.get_moder(), as_copy=True)
        client.send_message(bd.get_moder(), last_id)


@app.on_message(filters.chat(bd.get_moder()))
def send_post(client, message):
    # получаем запись в таблице
    for item in bd.get_data_in_table(message):
        username = item[0]
        msg_id = item[1]

    send = app.get_messages(username, msg_id)
    send.forward(bd.get_channel(), as_copy=True)


if __name__ == '__main__':
    print(datetime.today().strftime(f'%H:%M:%S | Bot launched.'))
    app.run()
