#!/bin/bash
sudo easy_install pip
pip install virtualenv
virtualenv env
source env/bin/activate
pip install flask
pip install selenium
pip install BeautifulSoup4
pip install redis
deactivate