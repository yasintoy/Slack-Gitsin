#!/bin/bash
SUPPORTED_PYTHON_VER=2
PYTHON_WARNING_MESSAGE="You should have python $SUPPORTED_PYTHON_VER in order to use Slack-Gitsin."

function setup {
  virtualenv -p python2.7 env
  source env/bin/activate
  pip install -r requirements.txt
  sudo apt-get install lolcat figlet zenity
}

if which python >/dev/null; then
  user_python_ver=$(python -c 'import sys; print(sys.version_info[0])')
  if [[ $user_python_ver -ne $SUPPORTED_PYTHON_VER ]]; then
    echo $PYTHON_WARNING_MESSAGE
  else
    setup
  fi
else
  echo $PYTHON_WARNING_MESSAGE
fi

