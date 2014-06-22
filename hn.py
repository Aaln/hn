#!/usr/bin/env python
#coding: utf8 

from flask import Flask, request, redirect, render_template, Markup
import os
from urllib import urlopen, urlencode
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import redis
import sys
import pymongo
from pymongo import MongoClient
import os

app = Flask(__name__)

# minimax - blog post about historical trends of hacker news

# natrual progression
# different ip
# credible usernames
# not new
# not the same users voting each other
# not so active
# block the known proxies
# unique users per ip
	# -x use colleges and highly populated places
# different ips for same user in frequent times
# block ip addresses from ec2, digitalocean, etc from making x amount of requests


def hnrequest(username, password, url):
	postId = url.split("?")[1].substring(3)

	driver = webdriver.Chrome("./chromedriver")
	login(driver, username, password)
	upvotePostById(driver, postId)

def upvotePostById(driver, postId):
	driver.get('https://news.ycombinator.com/newslogin?whence=news')
	time.sleep(.5)
	newestCount = 0
	while(0):
		allIds = driver.execute_script("""
			var allIds = [];
			var comheads = document.getElementsByClassName('comhead');
			for(var i = 0; i < comheads.length; i++) {
				var rawId = document.getElementsByClassName('comhead')[0].parentNode.parentNode.children[1].children[0].children[0].id;
				var thisId = rawId.substring(3, thisId.length);
				allIds.push(thisId);
			}
			return allIds;
		""")
		allTitles = driver.execute_script("""
			var allTitles = [];
			var comheads = document.getElementsByClassName('comhead');
			for(var i = 0; i < comheads.length; i++) {
				var title = comHeadDivs[i].parentNode.children[0].textContent;
				allTitles.push(title);
			}
			return allTitles;
		""")
		allComheads = driver.execute_script("""
			var allComheads = [];
			var comheads = document.getElementsByClassName('comhead');
			for(var i = 0; i < comheads.length; i++) {
				var rawcom = comheads[i].textContent.trim();
				allComheads.push(rawcom.substring(1, rawcom.length - 1));
			}
			return allComheads;
		""")
		for t in range(len(allIds)):
			if postId == allIds[t]:
				driver.execute_script("""
					var postLink = document.getElementById('%s');
					postLink.click();
					if(postlink.getAttribute('style').substring("visibility1").length === 19) {
						
					}
				""" %(postId))

		if newestCount == 5:
			break
		newestCount = newestCount + 1



def login(driver, username, password):
	driver.get('https://news.ycombinator.com/newslogin?whence=news')
	time.sleep(.5)
	driver.execute_script("""
		var username_input = document.getElementsByName('u')[0];
		var password_input = document.getElementsByName('p')[0];
		var submit_button = document.getElementsByTagName('input')[3];

		username_input.value = "%s";
		password_input.value = "%s";

		submit_button.click();
	""" % (username, password))

def hackNewsById(username, password, postId):
	driver = webdriver.Chrome("./chromedriver")
	driver.get('https://news.ycombinator.com/newslogin?whence=news')
	time.sleep(.5)
	driver.execute_script("""
		var username_input = document.getElementsByName('u')[0];
		var password_input = document.getElementsByName('p')[0];
		var submit_button = document.getElementsByTagName('input')[3];

		username_input.value = "%s";
		password_input.value = "%s";

		submit_button.click();
	""" % (username, password))
	time.sleep(.5)

	driver.execute_script("""
		var postLink = document.getElementById('up_%s');
		postLink.click();
	""" % (postId))

	time.sleep(.5)
	driver.quit()


def hackNewsByTitle(username, password, title):
	driver = webdriver.Chrome("./chromedriver")
	driver.get('https://news.ycombinator.com/newslogin?whence=news')
	time.sleep(.5)
	driver.execute_script("""
		var username_input = document.getElementsByName('u')[0];
		var password_input = document.getElementsByName('p')[0];
		var submit_button = document.getElementsByTagName('input')[3];

		username_input.value = "%s";
		password_input.value = "%s";

		submit_button.click();
	""" % (username, password))
	time.sleep(.5)
	driver.get('https://news.ycombinator.com/newest')
	newestCount = 0
	while(0):
		allIds = driver.execute_script("""
			var allIds = [];
			var comheads = document.getElementsByClassName('comhead');
			for(var i = 0; i < comheads.length; i++) {
				var rawId = document.getElementsByClassName('comhead')[0].parentNode.parentNode.children[1].children[0].children[0].id;
				var thisId = rawId.substring(3, thisId.length);
				allIds.push(thisId);
			}
			return allIds;
		""")
		allTitles = driver.execute_script("""
			var allTitles = [];
			var comheads = document.getElementsByClassName('comhead');
			for(var i = 0; i < comheads.length; i++) {
				var title = comHeadDivs[i].parentNode.children[0].textContent;
				allTitles.push(title);
			}
			return allTitles;
		""")
		allComheads = driver.execute_script("""
			var allComheads = [];
			var comheads = document.getElementsByClassName('comhead');
			for(var i = 0; i < comheads.length; i++) {
				var rawcom = comheads[i].textContent.trim();
				allComheads.push(rawcom.substring(1, rawcom.length - 1));
			}
			return allComheads;
		""")
		for t in range(len(allTitles)):
			if title == allTitles[t]:
				thisId = allIds[t]
				return thisId



def findPost(driver, postId, postTitle):
	allIds = driver.execute_script("""
		var allIds = [];
		var comheads = document.getElementsByClassName('comhead');
		for(var i = 0; i < comheads.length; i++) {
			var rawId = document.getElementsByClassName('comhead')[0].parentNode.parentNode.children[1].children[0].children[0].id;
			var thisId = rawId.substring(3, thisId.length);
			allIds.push(thisId);
		}
		return allIds;
	""")
	allTitles = driver.execute_script("""
		var allTitles = [];
		var comheads = document.getElementsByClassName('comhead');
		for(var i = 0; i < comheads.length; i++) {
			var title = comHeadDivs[i].parentNode.children[0].textContent;
			allTitles.push(title);
		}
		return allTitles;
	""")
	
	for t in range(len(allTitles)):
		if allTitles[t] == postTitle:
			upvotePost(driver, allIds[t])

def goToNextPage(driver):
	driver.execute_script("""
		var titles = document.getElementsByClassName('title');
		var moreLink = titles[titles.length - 1];
		moreLink.click();
	""")

hackNewsById('aaln', 'hello123', "7922748")
"""
@app.route('/', methods=['GET'])
def home():
	return render_template('home.html', error = "", userCount = userCount);
	#parse('aaln', 'reddit123', 'http')

	
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
"""

