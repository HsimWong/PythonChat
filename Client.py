# -*- coding: UTF-8 -*-
import socket
import time
import json
import hashlib
import groupClient as group 

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


	def sendToServer(self,string):
		self.sock.sendall(bytes(string.encode('utf-8')))

	def receiveFromServer(self):
		return str(self.sock.recv(1024), 'utf-8')

	def getEncrypted(self,string):
		return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

	def register(self):
		uname = ""
		pwd = ""
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

	def login(self):
		
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

	def makeFriend(self,uid):
		self.sendToServer(json.dumps({'command':'makeFriends', 'friend':uid}))
		print(self.receiveFromServer())

	def checkIfLogin(self):
		print()
		self.sendToServer(json.dumps({'command':'CheckIfLogIn', 'uid':self.uid})) 
		return print(self.receiveFromServer() == "YES")

	def logOff(self):
		loginStatus = False
		self.sendToServer(json.dumps({'command':"Exit"}))

	def startGroupChat(self):
		gc = group.GroupClient()
		gc.run(self.uname)
		



if __name__ == '__main__':
	vc = VerifyClient()
	vc.login()
	vc.startGroupChat()
	# vc = VerifyClient()
	# vc.checkIfLogin()
	# # vc.login()
	# vc.checkIfLogin()
	# vc.makeFriend(22)
	# vc.checkIfLogin()
	# vc.logOff()
	pass

