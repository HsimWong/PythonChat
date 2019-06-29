
# Connect to DB
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as sql

db = sql.connect(host = "2001:da8:216:e92f:9863:817d:849c:c75d",
                     user = "hardware",
                     passwd = "Wangxin",
                     db = "Chatroom" )
cursor = db.cursor()


def checkIfUnameOccupied(uname_str):
	cursor.execute("select * from users where userName = \'" + uname_str + "\';")
	results = cursor.fetchall()
	return not len(results) == 0
	
def verifyLogin(uname, pwdAES):
	cursor.execute("select * from users where userName = \'" + uname + "\';")
	results = cursor.fetchall()[0]
	return results[2] == pwdAES

def createUser(uname, pwdAES):
	# print("we are in")
	if not checkIfUnameOccupied(uname):
		# print("yes")
		cursor.execute("insert into users (userName, passwdHash) values (\'"\
			+ uname + '\', \'' + pwdAES +  '\');')
		db.commit()
		return True
	else:
		return False;

def getUID(uname):
	return isUser(uname)[1]

# def getUserName(uid):
# 	cursor.execute

def isUser(uname):
	uname = str(uname)
	rslt = cursor.execute("select * from users where " + ('userID = %s;'  if uname.isdigit() else "userName = \'%s\';")%str(uname)) == 1
	ret = (cursor.fetchone())
	userID, userName = (ret[0], ret[1]) if not ret == None else (None, None)
	# userID, userName = cursor.fetchone()[0:1] if rslt else 0

	return (rslt, userID, userName)
	
def getFriends(user):
	if isUser(user)[0]:
		cursor.execute("select friends from users where userID = %s;"%str(isUser(user)[1]))
		friends = eval('[%s]'%cursor.fetchone())
		return friends
	else:
		return None


def makeFriends(user1, user2):
	rslt1, userID1, uname1 = isUser(user1)
	rslt2, userID2, uname2 = isUser(user2)
	if rslt1 and rslt2 and (not userID2 == userID1):
		cursor.execute("select friends from users where userID = %s;"%str(userID1))
		ori_user1_friendList = cursor.fetchone()[0]
		ori_user1_friendList = "" if (ori_user1_friendList == None) else ori_user1_friendList
		new_user1_friendList = ori_user1_friendList + ('%d,'%userID2 if '%d,'%userID2 not in ori_user1_friendList else "")
		cursor.execute("update users set friends = '%s' where userID = %d;"%(new_user1_friendList, userID1))
		cursor.execute("select friends from users where userID = %s;"%str(userID2))
		ori_user2_friendList = cursor.fetchone()[0]
		ori_user2_friendList = "" if (ori_user2_friendList == None) else ori_user2_friendList
		new_user2_friendList = ori_user2_friendList + ('%d,'%userID1 if '%d,'%userID1 not in ori_user2_friendList else "")
		cursor.execute("update users set friends = '%s' where userID = %d;"%(new_user2_friendList, userID2))
		db.commit()
		return True
	else:
		return False
	

if __name__ == '__main__':
	# print(checkIfUnameOccupied("444"))
	print(makeFriends(24, 1))
	# print(makeFriends("1", "4"))