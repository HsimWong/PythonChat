# # -*- coding: UTF-8 -*-
# import socket

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65432    # Port to listen on (non-privileged ports are > 1023)

# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #  s.bind((HOST, PORT))
# #  s.listen()
# #  conn, addr = s.accept()
# #  with conn:
# #   print('Connected by', addr)
# #   while True:
# #    data = conn.recv(1024)
# #    if not data:
# #     break
# #    conn.sendall(data)
# SocketUnloged = []
# LoginSockets = {}   # {userid: socket_obj}

# def dealWithOneSocket(sock):

# def startDialog(socket1, socket2):
#    pass
# def manageOneSocket(sock):
#    pass

# def run():
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.bind((HOST, PORT))
#    s.listen()
#    connection_status, addr = s.accept()
#    with connection_status:
#       
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
				self.searchFriends(command)
				continue
			elif command['command'] == "makeFriends":
				self.makeFriends(command)
				continue
			elif command['command'] == "ChatToPerson":
				self.Chat(command)
				continue
			elif command['command'] == "Logoff":
				self.Logoff(command)
				continue
			elif command['command'] == "CheckFriendList":
				self.checkFriendList(command)
				continue
			elif command['command']	== "Exit":
				break
			elif command['command'] == "ifRegisNameValid":
				self.CheckRegisNameValid(command)
				continue
			else:
				self.sendToSocket("Your command is not correct\n>")
				continue
		self.sendToSocket("Disconnected from server")


	
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

	def checkIfUserLoggedIn(serf, uid):
		return (not (LoginSockets[uid] == None))


	def Login(self, msg):
		# if not LoginSockets[]
		uName, pwd = msg['uName'], msg['pwdHASH']
		isUser, UID, uName= sv.isUser(uName)
		# if UID not in LoginSockets.keys():
		if isUser:
			if sv.verifyLogin(uName, pwd):
				self.uid = UID 
				self.ifLogedIn = True
				LoginSockets.update({self.uid : self})
				self.sendToSocket("OK")
				# self.checkFriendList()
				return True
			else:
				self.sendToSocket("BAD")
				return False
		else:
			self.sendToSocket("BAD")
			return False
		# else:
		# 	self.sendToSocket("ANOTHERLOCATION")
		# 	return False

	def checkFriendList(self):
		friendsID = sv.getFriends(self.uid)
		ret_dic = {}
		for friend in friendsID:
			friendName = sv.isUser(friend)[3]
			ifOnline = friend
			ret_dic.update({friend:(friendName, ifOnline)})
		self.friendList = ret_dic


		return ret_dic


	def logOff(self):
		LoginSockets.pop(self.uid)
		# del self

	def searchFriend(self, msg):
		rslt, uid, uname = sv.isUser(msg['friend'])
		if rslt:
			return [uid, uname]
		else:
			return None

	def makeFriends(self, msg):
		rslt = sv.makeFriends(self.uid, msg['friend'])
		self.sendToSocket(("OK" if rslt else "FAILED"))

	# def ChatToPerson(self, msg): 
	# 	friend_id = msg['friend']
	# 	if


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