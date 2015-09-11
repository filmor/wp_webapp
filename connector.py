#! /usr/bin/python
# coding: utf-8

"""
	Connect to https://wordpress.org/plugins/json-api/
	
	Wordpress WebApp
	(gpl v3) by Tobias Sauer
    http://tobi.leichtdio.de
    part of
        - Dreifach Glauben : http://dreifachglauben.de
        - Leichtdio.de : http://leichtdio.de
    tobias [at] leichtdio . de
"""

import requests
import json

config = json.load(file("config.json", "r"))
		
class Connector:
	"""
		
	"""
	def __init__(self):
		self.config = json.load(file("config.json", "r"))
	
	def test_pingloop (self):
		pageno = 0
		r = requests.get("%s?page=%s" %(config["meta"]["api"], pageno))
		response = r.json()
		while len(response) != 0:
			
			# Endloop
			pageno += 1
			r = requests.get("%s/posts?page=%s" %(config["meta"]["api"], pageno))
			jsonfile = r.json()

	def ping (self, reset=False):
		"""
			first ping : create db
			next ping : update db
		"""
		#r = requests.get(config["meta"]["api"])
		#jsonfile = r.json()
		entrys = []
		pageno = 0
		url = "%s/posts?page=%s" %(config["meta"]["api"], pageno)
		r = requests.get(url)
		jsonfile = r.json()
		
		#print jsonfile
		
		while len(jsonfile) != 0:
			print "Page No %s" %(pageno)
			for entry in jsonfile:
				cats = []
				#print entry
				for cat in entry["terms"]["category"]:		
					cid = cat["ID"]
					while cid > self.config["category"]["highest"]:
						cid = cid - self.config["category"]["highest"]		
					cats.append([cat["name"],
								 cat["link"],
								 self.config["category"][str(cid)]])
		
				try:
					thumbnail = entry["featured_image"]["attachment_meta"]["sizes"]["thumbnail"]["url"]
				except KeyError:
					thumbnail = "http://placehold.it/42x42"
				
				new_entry = {
					"ID" : entry["ID"],
					"title" : entry["title"],
					"url" : entry["link"],
					"content" : entry["content"],
					"img" : entry["featured_image"]["attachment_meta"]["sizes"]["medium"]["url"],
					"thumb" : thumbnail,
					"author" : {
						"name" : entry["author"]["name"],
						"avatar" : entry["author"]["avatar"],
						"desc" : entry["author"]["description"]
						},
					"category" : cats
					}
				
				entrys.append(new_entry)
			# Endloop
			pageno += 1
			r = requests.get("%s/posts?page=%s" %(config["meta"]["api"], pageno))
			jsonfile = r.json()
		
		json.dump(entrys, file("posts.json", "w"))
	
	def get_post(self, post_id):
		jsonfile = json.load(file("posts.json", "r"))
		for entry in jsonfile:
			if entry["ID"] == post_id:
				return entry
		else:
			return False
	
	def get_all_post(self):
		jsonfile = json.load(file("posts.json", "r"))
		return jsonfile


if __name__ == "__main__":
	debug = Connector()
	#debug.initconf("http://dreifachglauben.de")
	#debug.get_all_post()
	debug.ping()
