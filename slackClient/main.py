#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import settings

import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import os
import slackclient
import time

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.filters import Always
from prompt_toolkit.interface import AcceptAction


from utils import TextUtils
from completer import Completer

from slack import Slack
from style import DocumentStyle

from threading import Event, Thread


def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def find_user_name(user_id):
    url = "https://slack.com/api/users.list?token={token}".format(token=settings.token)
    response = requests.get(url).json()
    for i in response["members"]:
        if i["id"] == user_id:
            return i["name"]
    return None

def get_alert(text):
    url = "https://slack.com/api/auth.test?token={token}".format(token=settings.token)
    response = requests.get(url).json()
    my_user_id = "<@" + response["user_id"] + ">"
    for i in text:
        if "text" in i:
            if my_user_id in i['text']:
                i["text"] = i["text"].replace(my_user_id, "@"+ find_user_name(response["user_id"]))
                os.system("notify-send -i " + settings.slack_logo + " 'you have new message' '{user} : {message}'".format(user=find_user_name(i["user"]), message=i['text']))


def check_notification():
    sc = slackclient.SlackClient(settings.token)
    if sc.rtm_connect():
        while True:
            get_alert(sc.rtm_read()) # send dictionary
            # print sc.rtm_read()
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

stop = call_repeatedly(2, check_notification) # call check_notification every 2 second

def main():
    """ 
         Start the Slack Client 
    """
    os.system("clear; figlet 'Slack Gitsin' | lolcat")
    history = FileHistory(os.path.expanduser("~/.slackHistory"))
    while True:
        try:
            text = prompt("slack> ", history=history,
                              auto_suggest=AutoSuggestFromHistory(),
                              on_abort=AbortAction.RETRY,
                              style=DocumentStyle,
                              completer = Completer(fuzzy_match=False,
                                                    text_utils=TextUtils() ),
                              complete_while_typing=Always(),
                              accept_action=AcceptAction.RETURN_DOCUMENT
            )
            slack = Slack(text)
            slack.run_command()
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == '__main__':
    main()