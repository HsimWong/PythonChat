# -*- coding: UTF-8 -*-
import socket
import time
import json
import hashlib
import groupClient as group 
from threading import Thread 

REGIS_PORT = 45678

class VerifyClient:
	def __init__(self):
		global REGISPORT
		self.HOST = '127.0.0.1'	# The server's hostname or IP address
		self.PORT = REGIS_PORT		# The port used by the server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.HOST, self.PORT))
		self.uid = 0
		self.uname = ""
		self.login_status = False
		self.ready = True 


	def sendToServer(self,string):
		self.sock.sendall(bytes(string.encode('utf-8')))

	def receiveFromServer(self):
		return str(self.sock.recv(1024), 'utf-8')

	def getEncrypted(self,string):
		return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

	def register(self):
		uname = ""
		pwd = ""
		self.ready = False
		while True:
			uname = input("Please input a user with at least one non-digital character\n>")
			command = json.dumps({'command':'ifRegisNameValid', 'uname':uname})
			# print(command)
			self.sendToServer(command)
			name_status = self.receiveFromServer()
			if name_status == "OK":
				break
			elif name_status == "NameOccupied":
				print("The name is Occupied, choose another one.\n>")
			elif name_status == "NameInvalid":
				print("The name is invalid, choose another one.\n>")
		pwd = self.getEncrypted(input("Please input your password.\n>"))
		self.sendToServer(json.dumps({'command':"Register", 'uName':uname, "pwdHASH":pwd}))
		regis_status = self.receiveFromServer() == "OK"
		if regis_status:
			print("You have successfully registered\n>")
		self.ready = True

	def login(self):
		self.ready = False
		while True:
			self.uname = input("Please input your username.\n>")
			pwd = self.getEncrypted(input("Please input your password.\n>"))
			self.sendToServer(json.dumps({"command":"Login", "uName":self.uname, "pwdHASH": pwd}))
			# rcv = receiveFromServer
			loginStatus = eval(self.receiveFromServer())
			if loginStatus[0] == 'OK':
				self.uid	= loginStatus[1]
				self.login = True
				# self.uname = uname
				break
			else:
				continue
		self.ready = True

	def makeFriend(self,uid):
		self.ready = False
		if not self.checkIfLogin():
			self.login()
		self.sendToServer(json.dumps({'command':'makeFriends', 'friend':uid}))
		print(self.receiveFromServer())
		self.ready = True

	def checkIfLogin(self):
		self.ready = False
		self.sendToServer(json.dumps({'command':'CheckIfLogIn', 'uid':self.uid})) 
		return self.receiveFromServer() == "YES"
		self.ready = True

	def checkIfOtherUserLogin(self, uid):
		self.sendToServer(json.dumps({'command':'CheckIfLogIn', 'uid':uid})) 
		return self.receiveFromServer() == "YES"

	def checkOtherUserInfo(self):
		self.ready = False
		token = str(input("Please input his/her username or user id:\n> "))
		self.sendToServer(json.dumps({'command':'searchFriends', 'friend': token}))
		print("id\t\tUserName\tOnline")
		dic = eval(self.receiveFromServer())
		# print(dic)
		for i in range(3):
			print(str(dic[i]), end = "\t\t")
			print(token if i == 2 else "", end = "")
		print()
		time.sleep(2)
		self.ready = True

	def logOff(self):
		self.ready = False
		loginStatus = False
		self.sendToServer(json.dumps({'command':"Exit"}))
		self.ready = False

	def startGroupChat(self):
		if not self.checkIfLogin():
			self.login()

		gc = group.GroupClient()
		gc.run(self.uname)

	def checkFriendList(self):
		self.ready = False
		self.sendToServer(str(json.dumps({'command':'CheckFriendList'})))
		fri_str = self.receiveFromServer()
		# print(fri_str)
		friend_dic = eval(fri_str)
		for friend in friend_dic.keys():
			print("Friend ID: %s	Friend Name: %s	Online Status: %s	"%(friend, friend_dic[friend][0], friend_dic[friend][1]))
		print()
		
		return friend_dic

	def checkIfFriend(self, friend_uid):
		self.sendToServer(json.dumps({'command':'CheckIfFriend', }))
		self.receiveFromServer()

	def chatToPerson(self, uid):
		# Check if friend
		# friend_uid = int(input("Please input the friends' id \n> "))
		# self.sendToServer(json.dumps({'command':'CheckIfFriend', 'friend_id':uid}))
		
		def ChatSending():
			print("The sending thread initiated...\n> ")
			while True:
				msg = input()
				print("You said:%s"%msg)
				if not msg == "quit":
					self.sendToServer(json.dumps({'command': 'ChatToPerson', 'toChat':"YES", 'friend_id':int(uid), 'msg':msg}))
				else:
					self.sendToServer(json.dumps({'command': 'ChatToPerson', 'toChat':"NO"}))

		def ChatReceive():
			print("The receiveing thread initiated...\n> ")
			while True:
				print(".", end = "")
				print(self.receiveFromServer())
				print("> ")
		ReceiveThread = Thread(target = ChatReceive).start()
		SendingThread = Thread(target = ChatSending).start()
		print("Don't get out")









		



if __name__ == '__main__':
	vc = VerifyClient()
	vc.login()
	
	pass

