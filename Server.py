# -*- coding: UTF-8 -*-
#2001:da8:216:e92f:9863:817d:849c:c75d
import socket, threading
import json
import ServerDB as sv
LoginSockets = {} #{userID: socket}


class ClientThread(threading.Thread):
	def __init__(self,clientAddress,clientsocket):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
		self.cAddr = clientAddress
		print ("New connection added: ", clientAddress)
		self.uid = -1
		self.ifLogedIn = False
		self.friendList = {}

	def run(self):
		global LoginSockets
		# print ("Connection from : ", clientAddress)
		#self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
		msg = ''
		while True:
			# self.sendToSocket("Please tell us what you would like to do\n>")
			try:
				data = self.csocket.recv(2048)
				msg = data
			except:
				print("client: %s lost connection."%self.cAddr )
				self.csocket.close()
				del self
				# exit()
			
			command = json.loads(msg)    #{"command":"Login..."...}

			if command['command'] == 'Login':
				self.ifLogedIn = self.Login(command)
				continue
			elif command['command'] == "Register":
				self.Register(command)
				continue
			elif command['command'] == 'CheckIfLogIn':
				self.checkStatus(command)
				continue
			elif command['command'] == "searchFriends":
				self.searchFriendInfo(command)
				continue
			elif command['command'] == "makeFriends":
				self.makeFriends(command)
				continue
			elif command['command'] == "ChatToPerson":
				self.Chat(command)
				continue
			elif command['command'] == "Logoff":
				self.Logoff()
				continue
			elif command['command'] == "CheckFriendList":
				self.checkFriendList()
				continue
			elif command['command'] == "CheckIfFriend":
				self.checkIfFriend()
				continue
			elif command['command']	== "Exit":
				break
			elif command['command'] == "ifRegisNameValid":
				self.CheckRegisNameValid(command)
				continue
			elif command['command'] == "SwitchToPersonal":
				continue

			else:
				self.sendToSocket("Your command is not correct\n>")
				continue
		self.sendToSocket("Disconnected from server")
		self.csocket.close()

	def sendToSocket(self, msg_str):
		self.csocket.send(bytes(msg_str, 'utf-8'))
		print(msg_str)

	def CheckRegisNameValid(self, msg):
		print("received from client: %s"%msg)
		self.sendToSocket("OK" if ((not sv.checkIfUnameOccupied(msg['uname']))\
			 and (not msg['uname'].isdigit())) else ("NameInvalid" if msg['uname'].isdigit()\
			  else "NameOccupied"))
		
	def Register(self, msg):
		print("StartRegister")
		#{cmd, uName, pwdHASH}
		if sv.createUser(msg['uName'], msg['pwdHASH']):
			self.sendToSocket("OK")
		else:
			self.sendToSocket("NameOccupied")

	def SocketIsLogedIn(self):
		return (self.uid >= 1)

	def checkStatus(self, msg):
		if msg['uid'] in LoginSockets.keys() and LoginSockets[msg['uid']] == self:
			self.sendToSocket("YES")
		else:
			self.sendToSocket("NO")
	
	def Login(self, msg):
		global LoginSockets
		# if not LoginSockets[]
		uName, pwd = msg['uName'], msg['pwdHASH']
		isUser, UID, uName= sv.isUser(uName)
		# if UID not in LoginSockets.keys():
		if isUser:
			if sv.verifyLogin(uName, pwd):
				self.uid = UID 
				self.ifLogedIn = True
				LoginSockets.update({self.uid : self})
				print(self.uid)
				print(self)
				print(LoginSockets[self.uid])
				print(self.uid in LoginSockets.keys())
				self.sendToSocket("('OK', %d)"%UID)
				# self.checkFriendList()
				return True
			else:
				self.sendToSocket("('BAD',)")
				return False
		else:
			self.sendToSocket("('BAD',)")
			return False
		# else:
		# 	self.sendToSocket("ANOTHERLOCATION")
		# 	return False

	def checkFriendList(self):
		global LoginSockets
		friendsID = sv.getFriends(self.uid)
		ret_dic = {}
		for friend in friendsID:
			friendName = sv.isUser(friend)[2]
			ifOnline = (friend in LoginSockets.keys())
			ret_dic.update({friend:(friendName, ifOnline)})
		self.friendList = ret_dic
		self.sendToSocket(str(ret_dic))
		return ret_dic

	def checkIfFriend(self, msg):
		friend_id = msg['friend_id']
		self.sendToSocket("YES" if msg['friend_id'] in self.checkFriendList().keys() else "NO")	

	def logOff(self):
		global LoginSockets
		LoginSockets.pop(self.uid)
		# del self

	def searchFriendInfo(self, msg):
		rslt, uid, uname = sv.isUser(msg['friend'])
		if rslt:
			self.sendToSocket(str((uid, uname, (uid in LoginSockets.keys()))))
			return [uid, uname]
		else:
			self.sendToSocket("(\"This user does not exist\",)")
			return None

	def makeFriends(self, msg):
		print(msg)
		print(self.uid)
		rslt = sv.makeFriends(self.uid, msg['friend'])
		self.sendToSocket(("OK" if rslt else "FAILED"))

	def checkIfFriendOnline(self, msg):
		global LoginSockets
		fri_uid = msg['friend']
		self.sendToSocket("OK" if fri_uid in LoginSockets.keys() else "NO")

	def ChatToSomeOne(self, raw_msg):
		if not self.checkStatus():
			self.sendToSocket("You are not yet logged in.\n")
			return
		else:
			if raw_msg['toChat'] == "YES":
				global LoginSockets
				friend_id = int(raw_msg['friend_id'])
				friend_socket = LoginSockets[friend_id]
				friend_socket.send(bytes("%s: %s\n"%(friend_id, raw_msg['msg']), 'utf-8'))
				self.sendToSocket("%s: %s\n"%(friend_id, raw_msg['msg']))
			else:
				return

def main():
	LOCALHOST = "127.0.0.1"
	PORT = 45678
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((LOCALHOST, PORT))
	print("Server started")
	print("Waiting for client request..")
	while True:
		server.listen()
		clientsock, clientAddress = server.accept()
		newthread = ClientThread(clientAddress, clientsock)
		print("new thread established...")
		newthread.start()

if __name__ == '__main__':
	main()