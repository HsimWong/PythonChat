# -*- coding: UTF-8 -*-
import socket
import time
import json
import hashlib



HOST = '127.0.0.1'	# The server's hostname or IP address
PORT = 45678		# The port used by the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
	


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
	uname = input("Please input your username.\n>")
	pwd = getEncrypted(input("Please input your password.\n>"))
	sendToServer(json.dumps({"command":"Login", "uName":uname, "pwdHASH": pwd}))
	loginStatus = receiveFromServer()
	print(loginStatus)

def makeFriend():
	uid = 1
	sendToServer(json.dumps({'command':'makeFriends', 'friend':uid}))
	print(receiveFromServer())











if __name__ == '__main__':
	# init()
	# register()
	print("Now, login")
	login()
	makeFriend()

	sock.close()


# if __name__ == '__main__':
# 	while True:
# 		string = input()
# 		byte_obj = bytes(string.encode('utf-8'))
# 		sock.sendall(byte_obj)
# 		# s.sendall(b'中国'.encode(encoding='UTF-8',errors='strict'))
# 		data = str(sock.recv(1024), 'utf-8')	
# 		print(data)
# 		# print('Received', repr(data).('utf-8'))
# 		time.sleep(1)

 
# import socket
# SERVER = "127.0.0.1"
# PORT = 45678
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((SERVER, PORT))
# client.sendall(bytes("This is from Client",'UTF-8'))
# while True:
# 	in_data = client.recv(1024)
# 	print("From Server :" ,in_data.decode())
# 	out_data = input()
# 	client.sendall(bytes(out_data,'UTF-8'))
# 	if out_data == 'bye':
# 		break
# client.close()