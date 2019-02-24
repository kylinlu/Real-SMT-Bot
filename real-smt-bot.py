#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import config
import os
import praw
import time

def bot_login():
	reddit = praw.Reddit(username = config.username,
		password = config.password,
		client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = "Real-SMT-Bot")

	return reddit

def run_bot(reddit, comments_replied_to):
	for comment in reddit.subreddit("all").comments(limit = None):
		if "persona" in comment.body.lower().split() and comment.id not in comments_replied_to and comment.author != reddit.user.me() and comment.subreddit != "megaten" and "bot" not in comment.author.name.lower():
			comment.reply("Weeb, play a real [Sheen Megoomi Tensay](https://youtu.be/zIjVvnO5lgM) \n\nHumanity's filth brought out this anti-Persona [Schwarzwelt](https://youtu.be/09Ty1p9tQEQ) \n\nJust look at how [cool](https://youtu.be/ut9ekAp2drs) and [sexy](https://youtu.be/TepXZN3Pw8o) mainline Shin Megami Tensei is! \n\n(And in case you thought *any* bit of Persona was hard, [LOL](https://youtu.be/J3ZMnOx5tzU)) \n\nLifeProTip: Kill your friends in [SMT4 Apocalypse](https://youtu.be/A3EFjFJgX3g)\n\nSincerely, r/Megaten \n\n***\n^I'm ^a ^bot *^bleep, ^bloop* ^| ^downvote ^to ^remove")
			comments_replied_to.append(comment.id)

			with open("comments_replied_to.txt", "a") as file:
				file.write(comment.id + "\n")

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as file:
			comments_replied_to = file.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))

	return comments_replied_to

def delete_negative_comments(comments):
	for comment in comments:
		if comment.score < 0:
			comment.delete()

reddit = bot_login()
comments_replied_to = get_saved_comments()
comments = reddit.user.me().comments.new(limit = None)

while True:
	try:
		delete_negative_comments(comments)
		run_bot(reddit, comments_replied_to)

	except Exception:
		continue