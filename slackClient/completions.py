#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import settings
import requests

# create slack channels list 
channels = {}
non_member_channels = {}
# get user_id
url = "https://slack.com/api/auth.test?token={token}".format(token=settings.token)
response = requests.get(url).json()
user_id = response["user_id"]

# get channels that our user already member to show him
url = "https://slack.com/api/channels.list?token={token}".format(token=settings.token)
response = requests.get(url).json()
for i in response["channels"]:
    if i["is_member"]:
        channels.update(
            {
                i["name"]: i["purpose"]["value"]
            }
        )
    else:
        non_member_channels.update(
            {
                i["name"]: i["purpose"]["value"]
            }
        )

# get user list
users = {}
url = "https://slack.com/api/users.list?token={token}".format(token=settings.token)
response = requests.get(url).json()
for i in response["members"]:
    users.update(
        {
            "@" + i["name"] : i["id"]
        }
    )


FREELANCER_POST_ID = str(8)
WHO_IS_HIRING_POST_ID = str(10)

SUBCOMMANDS = {

	"channels.history"  : "Fetches history of messages and events from a channel.",
	"channels.join"  	: "Joins a channel, creating it if needed.",
	"channels.list"  	: "Lists all channels in a Slack team.",
	"chat.postMessage"  : "Sends a message to a channel.",
	"files.upload"  	: "Upload an image/file",
	"channels.invite" 	: "Invites a user to a channels.",
	"channels.create" 	: "Creates a channels. ",
	"groups.list " 	    : "Lists groups that the calling user has access to.",
	"users.info"  	    : "Gets information about a channel.",
	"users.list"        : "Lists all users in a Slack team."

}
ARGS_OPTS_LOOKUP = {

    'channels.history': {
        'args': 'Show',
        'opts': list(channels.keys()),
    },
    'channels.join': {
        'args': '"Join"',
        'opts': list(non_member_channels.keys()),
    },
    'chat.postMessage': {
        'args': '"Send"',
        'opts': list(channels.keys()),
    },
    'channels.invite': {
        'args': '"invite"',
        'opts': list(channels.keys()),
    },

    'users.info': {
        'args': 'Show',
        'opts': list(users.keys()),
    },
        'files.upload': {
        'args': 'Upload',
        'opts': list(channels.keys()),
    }

}

META_LOOKUP = {
    '10': 'limit: int (opt) limits the posts displayed',
    '"(?i)(Python|Django)"': ('regex_query: string (opt) applies a regular '
                              'expression comment filter'),
    '1': 'index: int (req) views the post index',
    '"user"': 'user:string (req) shows info on the specified user',
    '--comments_regex_query ""': ('Filter comments with a regular expression'
                                  ' query (string)'),
    '-cq ""': ('Filter comments with a regular expression'
               ' query (string)'),
    '--comments': 'View comments instead of the url contents (flag)',
    '-c': 'View comments instead of the url contents (flag)',
    '--comments_recent': 'View only comments in the past hour (flag)',
    '-cr': 'View only comments in the past hour (flag)',
    '--comments_unseen': 'View only previously unseen comments (flag)',
    '-cu': 'View only previously unseen comments (flag)',
    '--comments_hide_non_matching': ('Hide instead of collapse '
                                     'non-matching comments (flag)'),
    '-ch': 'Hide instead of collapse non-matching comments (flag)',
    '--clear_cache': 'Clear the comment cache before executing.',
    '-cc': 'Clear the comment cache before executing.',
    '--browser': 'View in a browser instead of the terminal (flag)',
    '-b': 'View in a browser instead of the terminal (flag)',
    '--id_post ' + WHO_IS_HIRING_POST_ID: ('View matching comments from '
                                           'the (optional) post id instead'
                                           ' of the latest post (int)'),
    '-i ' + WHO_IS_HIRING_POST_ID: ('View matching comments from '
                                    'the (optional) post id instead'
                                    ' of the latest post (int)'),
    '--limit 10': 'Limits the number of user submissions displayed (int)',
    '-l 10': 'Limits the number of user submissions displayed (int)',
}
META_LOOKUP.update(SUBCOMMANDS)
