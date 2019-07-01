
import Client as cl 
import time
import groupClient as gc 



def main():
	vc = cl.VerifyClient()
	print("Welcome to the PythonChat System. \nWould you like to register or login?")
	while True:
		print(vc.HOST)
		print("1. Login\n2. Register\n >", end = "")
		command = input()
		# print(command)
		if command == "1":
			vc.login()
			break
		elif command == "2":
			vc.register()
			continue
		else:
			print("Illegal instruction! Please re-input")
			continue
	print("You have successfully logged in.")
	while True:
		print("You can do:")
		print("1. Check your friend list")
		print("2. Search a friend info")
		print("3. Make a friend with a user")
		print("4. Chat with one of your friend")
		print("6. Chat with all users using voice call")
		print("5. Chat with all users")
		print("7. Exit")
		print("> ", end = "")
		command = int(input())

		if command == 1:
			vc.checkFriendList()
			time.sleep(1)
			continue
		elif command == 2:
			print(vc.checkOtherUserInfo())
			continue
		elif command == 3:
			uid = int(input("Please input the ID of your Friend\n> "))
			vc.makeFriend(uid)
			continue
		elif command == 4:
			uid = int(input("Please input the ID of your Friend\n> "))
			vc.chatToPerson(uid)
			continue
		elif command == 5:
			continue
		elif command == 6:
			client = gc.GroupClient()
			client.run()
			continue
		elif command == 7:
			break
		else:
			print("Wrong command! Please re-input!")
			continue
	print("Good bye!")

if __name__ == '__main__':
	main()