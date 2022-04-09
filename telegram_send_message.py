import requests

def telegram_bot_sendtext(bot_token,bot_mesaj, id: str):
    bot_token = str(bot_token)
    bot_chatID = id
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(
        bot_chatID) + '&parse_mode=Markdown&text=' + bot_mesaj

    response = requests.get(url)

