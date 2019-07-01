import Client

class PrivateChatHandler():
	def __init__(self, sock1, sock2, self_port, host):
		server = socket(family = AF_INET, type = SOCK_STREAM)
		server.bind((host, self_port))
		BufferSize = 1024
		server.listen(5)
		print("Private Handler started")