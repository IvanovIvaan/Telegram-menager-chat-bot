from .dispatcher_bot import dispatcher
from aiogram.types import CallbackQuery
from .keyboards_bot import user_inline_keyboard
import sqlite3 
from .buttons_bot import button_delete_user


@dispatcher.callback_query()
async def callback_handler(callback: CallbackQuery):
    # 
    data_base = sqlite3.connect(database= 'instance/data.db')
    cursor = data_base.cursor()
    # 
    if callback.data == "user":
        cursor.execute("SELECT * FROM user")
        list_users = cursor.fetchall()
        for user in list_users:
            button_delete_user.callback_data= f"delete_user_{user[0]}"
            await callback.message.answer(
                text= f"ID: {user[0]} \nName: {user[1]} \nPassword: {user[2]} \nIs_admin: {user[3]}",
                reply_markup= user_inline_keyboard
            )
    #
    elif "delete_user" in callback.data: # якщо бот отримує в callback.data значення "delete_user", то:
        id_user = int(callback.data.split("_")[-1])
        """
        створюється об'єкт id_user, в якому одразу створюється список із значення callback.data, 
        значення в якому розділяються по нижнім підкреслюванням. 
        Потім обирається останнє значення й воно записується в нашому об'єкті 
        з цілочисленним типом даних.
        """
        cursor.execute("DELETE FROM user WHERE id = ?", (id_user,))
        """
        за допомогою функції execute задаємо команду "видалити значення із стовпця "user", 
        який має id = id_user (тобто цілочислене, останнє значення із списку, створеного раніше із калбек.дати)". 
        Команду задаємо датабазі за допомогою капслока.
        (id = ? - означає, що замість знаку питання підставиться наступне значення після задання коду в функції execute модуля cursor)
        """
        await callback.message.delete() # задаємо асинхрону команду чат-боту видалити сповіщення, значення калбеку якого увійшло в умову

    #
    data_base.commit() #задіяти код, заданий датабазі
    data_base.close() #закрити датабазу, щоб не виникло помилки

# 25:   id_user = ['delete', 'user', '1'] => id_user = 1 