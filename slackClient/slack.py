#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import click
import requests
import settings
import os
import subprocess
import time
import slackclient  # for real time parts

from prettytable import PrettyTable
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from completions import users
from style import DocumentStyle


class Slack(object):
    def __init__(self, text):
        self.text = text

    def get_channels_list(self):
        # create slack channels list
        channels = []
        url = "https://slack.com/api/channels.list?token={token}".format(token=settings.token)
        response = requests.get(url).json()
        return response["channels"]

    def channels_join(self, name):
        url = "https://slack.com/api/channels.join?token={token}&name={name}".format(token=settings.token,
                                                                                     name=name)
        response = requests.get(url).json()
        if response["ok"]:
            os.system("figlet 'Joined' | lolcat")
            time.sleep(2)
            os.system("clear")
        else:
            print "something goes wrong :( (\u001b[1m\u001b[31m " + response["error"] + "\u001b[0m)"

    def channels_history(self, channel_name):
        # Retrieve channel id by using channel_name
        channel_id = self.find_channel_id(channel_name)
        url = "https://slack.com/api/channels.history?token={token}&channel={channel_id}".format(token=settings.token,
                                                                                                 channel_id=channel_id)
        response = requests.get(url).json()
        if response['ok']:
            self.print_history(response, channel_name)
        else:
            print "something goes wrong!"

    def post_message(self, channel_name):
        # self.channels_history(channel_name)
        os.system("echo '\u001b[1m\u001b[31m  To mention a user write @ while chatting \u001b[0m'")
        text = prompt("your message > ", completer=WordCompleter(users))
        channel_id = self.find_channel_id(channel_name)
        url = "https://slack.com/api/chat.postMessage?token={token}&channel={channel_id}&text={text}&as_user=true&link_names=1".format(
            token=settings.token,
            text=text,
            channel_id=channel_id)
        response = requests.get(url).json()
        # TODO : retrieve message history and print to screen while chatting
        if response["ok"]:
            os.system("figlet 'Sent' | lolcat")
            time.sleep(2)
            os.system("clear")
        else:
            print "something goes wrong :( (\u001b[1m\u001b[31m " + response["error"] + "\u001b[0m)"

    def channels_invite(self, channel_name):
        channel_id = self.find_channel_id(channel_name)
        invites = prompt("send invites -> ", completer=WordCompleter(users),
                         style=DocumentStyle)
        for i in invites.split(" "):
            user_id = self.find_user_id(i.strip("@"))
            url = "https://slack.com/api/channels.invite?token={token}&channel={channel_id}&user={user}".format(
                token=settings.token,
                channel_id=channel_id,
                user=user_id)
            response = requests.get(url).json()
            if response["ok"]:
                os.system("figlet 'Invited " + i + "' | lolcat")
                time.sleep(2)
                os.system("clear")
            else:
                print "something goes wrong :( (\u001b[1m\u001b[31m " + response["error"] + "\u001b[0m)"

    def channels_create(self):
        os.system("clear")
        fields = ["name", "purpose(OPTINAL)", "send invite"]
        for i in fields:
            if i == "name":
                name = raw_input("\u001b[1m\u001b[31m channel name -> \u001b[0m")
            elif i == "purpose(OPTINAL)":
                purpose = raw_input("\u001b[1m\u001b[31m purpose of the channel(OPTINAL) : \u001b[0m")
            else:
                invites = prompt("send invites -> ", completer=WordCompleter(users),
                                 style=DocumentStyle)

        url = "https://slack.com/api/channels.create?token={token}&name={name}&purpose={purpose}".format(
            token=settings.token,
            name=name,
            purpose=purpose)
        response = requests.get(url).json()
        # TODO :  send channel and user_id to channels_invite
        if response["ok"]:
            os.system("figlet 'Created' | lolcat")
            time.sleep(2)
            os.system("clear")

    def users_list(self):
        # get user list
        os.system("clear")
        users = {};
        url = "https://slack.com/api/users.list?token={token}".format(token=settings.token)
        response = requests.get(url).json()
        text = PrettyTable(["name", "tz", "tz_label", "email"])
        for i in response["members"]:
            text.add_row([i["name"], str(i["tz"]), str(i["tz_label"]), str(i["profile"]["email"])])

        # os.system("echo '" + text + "' | lolcat")
        print text

    def users_info(self, user_name):
        user_id = self.find_user_id(user_name.strip("@"))
        url = "https://slack.com/api/users.info?token={token}&user={user_id}".format(token=settings.token,
                                                                                     user_id=user_id)
        response = requests.get(url).json()
        if response["ok"]:
            self.print_users_info(response['user'])
        else:
            print "something goes wrong :( (\u001b[1m\u001b[31m " + response["error"] + "\u001b[0m)"

    def file_upload(self, channel_name):
        os.system("clear")
        channel_id = self.find_channel_id(channel_name)
        fields = ["file", "content", "filename", "title", "initial_comment"]
        for i in fields:
            if i == "file":
                os.system("echo 'opening the file dialog. wait...' ")
                file = subprocess.check_output(['zenity', '--file-selection'])
                os.system("echo '\u001b[1m\u001b[31m file : \u001b[0m'" + file + "'")
            elif i == "content":
                content = raw_input("\u001b[1m\u001b[31m content : \u001b[0m")
            elif i == "filename":
                filename = raw_input("\u001b[1m\u001b[31m filename : \u001b[0m")
            elif i == "title":
                title = raw_input("\u001b[1m\u001b[31m title : \u001b[0m")
            else:
                initial_comment = prompt("add comment : ", completer=WordCompleter(users),
                                         style=DocumentStyle)
        url = "https://slack.com/api/files.upload?token={token}&content={content}&filename={filename}&channels={channel_id}&title={title}&initial_comment={initial_comment}".format(
            token=settings.token,
            content=content,
            filename=filename,
            channel_id=channel_id,
            title=title,
            initial_comment=initial_comment)
        response = requests.get(url).json()
        if response["ok"]:
            os.system("figlet 'Uploaded!' | lolcat")
            time.sleep(2)
            os.system("clear")
        else:
            print "something goes wrong :( (\u001b[1m\u001b[31m " + response["error"] + "\u001b[0m)"

    def find_channel_id(self, channel_name):
        url = "https://slack.com/api/channels.list?token={token}".format(token=settings.token)
        response = requests.get(url).json()
        for i in response["channels"]:
            if i["name"] == channel_name:
                return i["id"]
        return None

    def find_user_id(self, user_name):
        url = "https://slack.com/api/users.list?token={token}".format(token=settings.token)
        response = requests.get(url).json()
        for i in response["members"]:
            if i["name"] == user_name:
                return i["id"]
        return None

    def find_user_name(self, user_id):
        url = "https://slack.com/api/users.list?token={token}".format(token=settings.token)
        response = requests.get(url).json()
        for i in response["members"]:
            if i["id"] == user_id:
                return i["name"]
        return None

    def print_history(self, response, channel_name):
        os.system("clear; figlet '" + channel_name + "' | lolcat")
        response["messages"].reverse()
        text = ""
        for i in response["messages"]:
            if "user" in i:
                text += "\033[31m" + self.find_user_name(i["user"]) + "\033[0m" + "\t\t"
            elif "username" in i:
                text += "\033[31m" + (i["username"].encode('ascii', 'ignore').decode('ascii')) + "\033[0m" + "\t"
            text += "\033[93m" + time.ctime(float(i["ts"])) + "\033[0m" + "\n"
            # replace username_id with username
            if "<@" in i["text"]:
                i["text"] = "<" + i["text"].split("|")[1]
            text += (i["text"].encode('ascii', 'ignore').decode('ascii')) + "\n\n"
            os.system("echo ' " + text + "'")
            text = ""

    def print_channels_list(self, response):
        os.system("clear; figlet '" + "All Channels" + "' | lolcat")
        text = ""
        for i in response:
            text += i["name"] + "\t\t" + "(created {when})\n".format(when=time.ctime(float(i["created"])))
        # print and reset text
        os.system("echo ' " + text + "' | lolcat")

    def print_users_info(self, response):
        os.system("clear; figlet '" + "User Info" + "' | lolcat")
        text = "name : " + response["name"] + "\n"
        for (key, value) in response["profile"].items():
            if type(value) == "str":
                text += key + " - > " + value + "\n"
            else:
                text += key + " - > " + str(value) + "\n"
        os.system("echo '" + text + "' | lolcat")

    def run_command(self):
        try:
            split_text = self.text.split(" ")
            if split_text[1] == "channels.list":
                response = self.get_channels_list()
                self.print_channels_list(response)
            elif split_text[1] == "channels.join":
                if len(split_text) < 4:
                    print "Please enter values properly"
                else:
                    self.channels_join(split_text[3])
            elif split_text[1] == "channels.history":
                if len(split_text) < 4:
                    print "Please enter values properly!"
                else:
                    self.channels_history(split_text[3])  # send channel_name
            elif split_text[1] == "chat.postMessage":
                self.post_message(split_text[3])
            elif split_text[1] == "channels.invite":
                self.channels_invite(split_text[3])  # send channel_name
            elif split_text[1] == "channels.create":
                self.channels_create()
            elif split_text[1] == "users.list":
                self.users_list()
            elif split_text[1] == "users.info":
                self.users_info(split_text[3])
            elif split_text[1] == "files.upload":
                self.file_upload(split_text[3])
        except:
            print "something goes wrong!"
