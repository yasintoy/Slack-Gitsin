#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import settings

import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

import os
import signal
import slackclient  #for real time parts
import time

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.filters import Always
from prompt_toolkit.interface import AcceptAction
from prompt_toolkit.token import Token
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys

from utils import TextUtils
from completer import Completer

from slack import Slack
from style import DocumentStyle

from threading import Event, Thread

manager = KeyBindingManager.for_prompt()


def find_user_name(user_id):
    url = "https://slack.com/api/users.list?token={token}".format(token=settings.token)
    response = requests.get(url).json()
    for i in response["members"]:
        if i["id"] == user_id:
            return i["name"]
    return None


def get_alert(text):
    #TODO : add notification sound
    url = "https://slack.com/api/auth.test?token={token}".format(token=settings.token)
    response = requests.get(url).json()
    my_user_id = "<@" + response["user_id"] + ">"
    for i in text:
        if "text" in i:
            if my_user_id in i['text']:
                i["text"] = i["text"].replace(my_user_id, "@" + find_user_name(response["user_id"]))
                if os.name == "posix":
                    cmd = """osascript -e 'display notification "{message}" with title "{title}" ' """.format(message=find_user_name(i["user"]) + " : " + i['text'], title="You have a new message")
                    os.system(cmd)
                else:
                    os.system(
                        "notify-send -i " + settings.slack_logo + " 'you have new message' '{user} : {message}'".format(
                            user=find_user_name(i["user"]), message=i['text']))


def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)

    Thread(target=loop).start()
    return stopped.set


def check_notification():
    sc = slackclient.SlackClient(settings.token)
    if sc.rtm_connect():
        while True:
            get_alert(sc.rtm_read())  # send dictionary
            # print sc.rtm_read()
    else:
        print "Connection Failed, invalid token?"


stop = call_repeatedly(2, check_notification)  # call check_notification every 2 second


def get_bottom_toolbar_tokens(cli):
    return [(Token.Toolbar, ' F10 : Exit ')]


@manager.registry.add_binding(Keys.F10)
def _(event):
    def exit():
        """ 
            Quit when the `F10` key is pressed
        """
        pid = os.getpid()
        stop()  # stop thread
        os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL
        quit()  # exit the program

    event.cli.run_in_terminal(exit)


def main():
    """ 
         Start the Slack Client 
    """
    os.system("clear; figlet 'Slack Gitsin' | lolcat")
    history = FileHistory(os.path.expanduser("~/.slackHistory"))
    while True:
        text = prompt("slack> ", history=history,
                      auto_suggest=AutoSuggestFromHistory(),
                      on_abort=AbortAction.RETRY,
                      style=DocumentStyle,
                      completer=Completer(fuzzy_match=False,
                                          text_utils=TextUtils()),
                      complete_while_typing=Always(),
                      get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                      key_bindings_registry=manager.registry,
                      accept_action=AcceptAction.RETURN_DOCUMENT
        )
        slack = Slack(text)
        slack.run_command()


if __name__ == '__main__':
    main()