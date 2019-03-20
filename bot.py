import os

import requests
from telegram.ext import CommandHandler, RegexHandler, Updater

from config import URL, PORT, USER_ID, JIRA_TOKEN
from utils import format_thousands


class Bot:
    def __init__(self, token, debug=False):
        self._token = token
        self._updater = Updater(token)
        self._debug = debug

        self._session = requests.Session()

        self._init_handlers()
    
    def run(self):
        self._updater.start_webhook(listen='0.0.0.0', port=PORT,
                                    url_path=self._token)
        self._updater.bot.set_webhook(URL + self._token)
        self._updater.idle()
    
    def _init_handlers(self):
        self._updater.dispatcher.add_handler(CommandHandler("start", self._start))
        self._updater.dispatcher.add_handler(CommandHandler("help", self._help))
        self._updater.dispatcher.add_handler(CommandHandler("send", self._send))

    def _start(self, bot, update):
        user_id = str(update.message.from_user.id)
        if user_id == USER_ID:
            update.message.reply_text('Hello, Leyla! :)')
        else:
            update.message.reply_text('Who are you? {}'.format(user_id))

    def _send(self, bot, update):
        user_id = str(update.message.from_user.id)
        if user_id == USER_ID:
            headers = {'Authorization': 'Basic {}'.format(JIRA_TOKEN)}
            data = {
                "fields":{"project": {"key": "NOTIFY"},
                          "assignee": {"name":"lkhatbullina"},
                          "priority": {"name": "Lowest"},
                          "summary": update.message.text[len("/send "):],
                          "issuetype": {"name": "Task"}
                          }
            }
            url = "https://jira.iponweb.net/rest/api/2/issue/"
            response = self._session.post(url, headers=headers, data=data)
            print(response.status_code)
            print(response.text)

            update.message.reply_text(str(response.status_code) + "\n" + response.text)

    def _help(self, bot, update):
        update.message.reply_text('Help!')

