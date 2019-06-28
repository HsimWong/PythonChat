# -*- coding: UTF-8 -*-
import socket
import time
import json
import hashlib



HOST = '127.0.0.1'	# The server's hostname or IP address
PORT = 45678		# The port used by the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
uid = 0
login = False


def sendToServer(string):
	sock.sendall(bytes(string.encode('utf-8')))

def receiveFromServer():
	return str(sock.recv(1024), 'utf-8')

def getEncrypted(string):
	return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

def register():
	uname = ""
	pwd = ""
	while True:
		uname = input("Please input a user with at least one non-digital character\n>")
		command = json.dumps({'command':'ifRegisNameValid', 'uname':uname})
		# print(command)
		sendToServer(command)
		name_status = receiveFromServer()
		if name_status == "OK":
			break
		elif name_status == "NameOccupied":
			print("The name is Occupied, choose another one.\n>")
		elif name_status == "NameInvalid":
			print("The name is invalid, choose another one.\n>")
	pwd = getEncrypted(input("Please input your password.\n>"))
	sendToServer(json.dumps({'command':"Register", 'uName':uname, "pwdHASH":pwd}))
	regis_status = receiveFromServer() == "OK"
	if regis_status:
		print("You have successfully registered\n>")

def login():
	global uid
	while True:
		uname = input("Please input your username.\n>")
		pwd = getEncrypted(input("Please input your password.\n>"))
		sendToServer(json.dumps({"command":"Login", "uName":uname, "pwdHASH": pwd}))
		# rcv = receiveFromServer
		loginStatus = eval(receiveFromServer())
		if loginStatus[0] == 'OK':
			uid	= loginStatus[1]
			login = True
			break
		else:
			continue

def makeFriend(uid):
	
	sendToServer(json.dumps({'command':'makeFriends', 'friend':uid}))
	print(receiveFromServer())

def checkIfLogin():
	global uid
	print(uid)
	sendToServer(json.dumps({'command':'CheckIfLogIn', 'uid':uid})) 
	return receiveFromServer() == "YES"

def logOff():
	loginStatus = False
	sendToServer(json.dumps({'command':"Exit"}))











if __name__ == '__main__':
	# init()
	# register()
	checkIfLogin()
	print("Now, login")
	login()
	checkIfLogin()
	logOff()
	# makeFriend()


	sock.close()

