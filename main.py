import telebot
from mcrcon import MCRcon

BOT_TOKEN = "7731318728:AAFCdxIiaB8yHlhFR1N5wsXQL079INlqsG8"
RCON_HOST = "donator38.gamely.pro"
RCON_PORT = 20614
RCON_PASSWORD = "12345678"
ALLOWED_USERS = ["absolute_fqwfdcv"] 

bot = telebot.TeleBot(BOT_TOKEN)

def send_rcon_command(command):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command(command)
        return response
    except Exception as e:
        return f"Ошибка: {str(e)}"

def restricted(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.username not in ALLOWED_USERS:
            bot.reply_to(message, "У вас нет прав для использования этой команды.")
            return
        return func(message, *args, **kwargs)
    return wrapper

@bot.message_handler(commands=['allow_user'])
@restricted
def allow_user(message):
    try:
        username = message.text.split()[1]
        if username not in ALLOWED_USERS:
            ALLOWED_USERS.append(username)
            bot.reply_to(message, f"Пользователь с username @{username} добавлен в список разрешённых.")
        else:
            bot.reply_to(message, "Этот пользователь уже есть в списке разрешённых.")
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите корректный username пользователя. Пример: /allow_user username")

@bot.message_handler(commands=['remove_user'])
@restricted
def remove_user(message):
    try:
        username = message.text.split()[1]
        if username in ALLOWED_USERS:
            ALLOWED_USERS.remove(username)
            bot.reply_to(message, f"Пользователь с username @{username} удалён из списка разрешённых.")
        else:
            bot.reply_to(message, "Этот пользователь не найден в списке разрешённых.")
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите корректный username пользователя. Пример: /remove_user username")

@bot.message_handler(commands=['list_users'])
@restricted
def list_users(message):
    if ALLOWED_USERS:
        users_list = "Список разрешённых пользователей:\n" + "\n".join(f"@{user}" for user in ALLOWED_USERS)
        bot.reply_to(message, users_list)
    else:
        bot.reply_to(message, "Список разрешённых пользователей пуст.")

# Команда /list: список игроков на сервере
@bot.message_handler(commands=['list'])
def list_players(message):
    response = send_rcon_command("list")
    bot.reply_to(message, response)

# Команда /plugins: список плагинов на сервере
@bot.message_handler(commands=['plugins'])
def list_plugins(message):
    response = send_rcon_command("plugins")
    bot.reply_to(message, response)

# Команда /whitelist add: добавить игрока в whitelist
@bot.message_handler(commands=['whitelist_add'])
@restricted
def whitelist_add(message):
    try:
        player_name = message.text.split()[1]
        response = send_rcon_command(f"whitelist add {player_name}")
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите имя игрока. Пример: /whitelist_add player_name")

# Команда /whitelist list: показать список игроков в whitelist
@bot.message_handler(commands=['whitelist_list'])
@restricted
def whitelist_list(message):
    response = send_rcon_command("whitelist list")
    bot.reply_to(message, response)

# Команда /whitelist remove: удалить игрока из whitelist
@bot.message_handler(commands=['whitelist_remove'])
@restricted
def whitelist_remove(message):
    try:
        player_name = message.text.split()[1]
        response = send_rcon_command(f"whitelist remove {player_name}")
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите имя игрока. Пример: /whitelist_remove player_name")

# Команда /ban_minecraft: забанить игрока на сервере
@bot.message_handler(commands=['ban_minecraft'])
@restricted
def ban_player(message):
    try:
        player_name = message.text.split()[1]
        response = send_rcon_command(f"ban {player_name}")
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите имя игрока. Пример: /ban_minecraft player_name")

# Команда /stats: показать статистику сервера
@bot.message_handler(commands=['stats'])
def server_stats(message):
    response = send_rcon_command("debug report")
    bot.reply_to(message, response if response else "Не удалось получить статистику сервера.")

# Команда /help: вывод списка доступных команд
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Доступные команды:\n"
        "/list - Список игроков на сервере\n"
        "/plugins - Список плагинов на сервере\n"
        "/whitelist_add [имя] - Добавить игрока в whitelist\n"
        "/whitelist_list - Показать список игроков в whitelist\n"
        "/whitelist_remove [имя] - Удалить игрока из whitelist\n"
        "/ban_minecraft [имя] - Забанить игрока на сервере\n"
        "/stats - Показать статистику сервера (выклл)\n"
        "/allow_user [username] - Добавить пользователя в список разрешённых\n"
        "/remove_user [username] - Удалить пользователя из списка разрешённых\n"
        "/list_users - Показать список разрешённых пользователей\n\n"
        "Создатель бота - @absolute_fqwfdcv"
    )
    bot.reply_to(message, help_text)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
