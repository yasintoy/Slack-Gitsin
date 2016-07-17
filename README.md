# ![SlackGitsin](screen_shots/logo.jpg)

The Problem
=================

> *We have Slack we use in our office using the Windows stand alone since the Chrome based app seems to not show notifications in the bar (highlighting the app when you have a waiting message).*
> *Nearly every day Slack has to be manually closed via task manager (all users at random times) because Slack is taking up nearly all CPU and memory on the PCs.*
> *Is this a known issue and if so is there any solution?*
> *-[Source](https://www.reddit.com/r/Slack/comments/3fy494/slack_taking_up_a_lot_of_system_resources/)

## Are you kidding me? "8 GB ought to be enough for everyone", Don't be ridiculous.

`Let me show you an example : ` A mix of pycharm, slack, vagrant and chrome : 
# ![](screen_shots/marcosmemory.jpg)


# ![](screen_shots/anim.gif)

## Installation(it's not finished)
**For Linux :**
```
  git clone https://github.com/yasintoy/Slack-Gitsin/
  cd Slack-Gitsin
  sudo apt-get install lolcat figlet zenity
  virtualenv env
  source env/bin/active
  pip install -r requirements.txt 

```

**For Mac : (TODO)** 
```
  git clone https://github.com/yasintoy/Slack-Gitsin/
  cd Slack-Gitsin
  brew install lolcat figlet zenity # if brew doesn't exist install it
  virtualenv env
  source env/bin/active
  pip install -r requirements.txt 

```

**Overview with some example screenshots**

# ![](screen_shots/overview.png)


## Create channel

   You can easily create slack channel by using the `SlackClient`

# ![image](screen_shots/channel_create_screen.png)

## Show channel messages

   (Message will chance)You can easily create slack channel by using the `SlackClient`

# ![image](screen_shots/history_screen.png)

## Send a post to channel

   (Message will chance)You can easily create slack channel by using the `SlackClient`

# ![image](screen_shots/channel_post_screen.png)


## List all Slack channels

   (Message will chance)You can easily create slack channel by using the `SlackClient`

# ![image](screen_shots/channel_list_screen.png)

## Join a channels that unmember

   (Message will chance)You can easily create slack channel by using the `SlackClient`

# ![image](screen_shots/channel_join_screen.png)


## Upload a file into slack channel

    (Message will chance)You can easily create slack channel by using the `SlackClient`

- First, choice file upload option
# ![image](screen_shots/upload_file_menu.png)

- Then, choice file by using the file dialog
# ![image](screen_shots/opened_file_dialog.png)

- Finally, fill out the screen
# ![image](screen_shots/file_upload_process.png)

