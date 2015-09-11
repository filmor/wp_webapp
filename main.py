#! /usr/bin/python
# coding: utf-8

"""
	Wordpress WebApp using bottle.py
	and JSON Api ( https://wordpress.org/plugins/rest-api/ )
	
    (gpl v3) by Tobias Sauer
    http://tobi.leichtdio.de
    part of
        - Dreifach Glauben : http://dreifachglauben.de
        - Leichtdio.de : http://leichtdio.de
    tobias [at] leichtdio . de
"""
	
from bottle import route, run, template, error, static_file, debug
import json

import os.path

import connector


pointer = connector.Connector()


@route('/css/<css>')
def server_static(css):
    return static_file(css, root="css")
    
@route('/fonts/<fontfile>')
def server_static(fontfile):
	return static_file(fontfile, root="fonts")

@route('/js/<js_lib>')
def server_static(js_lib):
    return static_file(js_lib, root="js")

@route('/images/<filename:re:.*\.png|.*\.jpg>')
def send_image(filename):
    if ".jpg" in filename:
        return static_file(filename, root="images", mimetype="image/jpeg")
    elif ".png" in filename:
        return static_file(filename, root='images', mimetype='image/png')

@error(404)
def error404(error):
    return 'Nothing here, sorry'


@route('/article/<article_id>')
def article(article_id):
	postdata = pointer.get_post(int(article_id))
	config = json.load(file("config.json", "r"))
	attrb = {"meta" : config["meta"],
			 "social" : config["social"],
			 "sharelinks" : config["sharelinks"],
			 "entry" : postdata,
	}
	attrb["meta"]["url"] = postdata["url"]
	print config["meta"]
	
	return template("blog_article.html", attrb)

@route('/ping/<passwd>')
def update(passwd):
	config = json.load(file("config.json", "r"))
	if passwd == config["pingpasswd"]:
		
		pointer.ping()
		return "Done."
	return "None."

@route('/')
def blogwebapp():
	if not os.path.isfile("posts.json"):
		pointer.ping()
	
	config = json.load(file("config.json", "r"))
	attrb = {"meta" : config["meta"],
			 "social" : config["social"],
			 "sharelinks" : config["sharelinks"],
			 "url" : config["meta"]["url"],
	}
	attrb["entrys"] = pointer.get_all_post()
	return template("blog_rachet.html", attrb)


debug(True)
### Add your Ip to test with a mobiledevice
run(host='192.168.1.162', port=8000, debug=False, reloader=True)
