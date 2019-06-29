import Client as cl 



def main():
	vc = cl.VerifyClient()
	print("Welcome to the PythonChat System. \nWould you like to register or login?")
	while True:
		print(vc.HOST)
		print("1. Login\n2. Register")
		command = input()
		# print(command)
		if command == "1":
			vc.login()
			break
		elif command == "2":
			vc.register()
			break
		else:
			print("Illegal instruction! Please re-input")
	print("")


if __name__ == '__main__':
	main()