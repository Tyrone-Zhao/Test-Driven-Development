from fabric.api import run


def install_jslint():
    run("sudo apt-get install python-software-properties -y"
        " && curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -"
        " && sudo apt-get install nodejs -y"
        " && sudo npm install -g nrm"
        " && nrm use taobao"
        " && sudo npm install -g jslint")
