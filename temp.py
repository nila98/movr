import MySQLdb

# connect
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",
db="main")

cursor = db.cursor()

# execute SQL select statement
_userID = 27
cursor.execute("SELECT TitleID FROM UserTitle WHERE UserID = %s",(_userID,))

data = cursor.fetchall()#data = ((1L,), (2L,), (7L,)) type:tuples
inputMovies = [item[0] for item in data]#inputMovies = [1L,2L,7L] type:list

tagList=[]

for item in data:
	cursor.execute("select keyword_id from movie_keyword where movie_id = %s",item)
	tagList.extend([item[0] for item in cursor.fetchall()])


cursor.execute("SELECT * FROM UserTitle")
allUsers = cursor.fetchall()

userOnly = [item[0] for item in allUsers]
unique = []
[unique.append(item) for item in userOnly if item not in unique]

userOnly = unique
movieOnly = []

curr = userOnly[0]
currList = []
for item in allUsers:
	if curr == item[0]:
		currList.append(item[1])
	else:
		movieOnly.append(currList)
		currList = []
		currList.append(item[1])
		curr = item[0]

movieOnly.append(currList)

sharedTags = []
for ind,item in enumerate(userOnly):
	tempShareTags = []
	if item != _userID:
		tempMovies = list(movieOnly[ind])
		for i in tempMovies:
				#print i
			        cursor.execute("select keyword_id from movie_keyword where movie_id = %s",(i,))
				temp0 = cursor.fetchall()
			        tempShareTags.extend([x[0] for x in temp0])
		
	sharedTags.append(tempShareTags)

truShare = []
truNum=[]
for item in sharedTags:
	sharetemp = list(set(item).intersection(tagList))
	truShare.append(sharetemp)
	truNum.append(len(sharetemp))

#print userOnly
#print truNum
#print truShare
print inputMovies
truMovie = []
truMovcount = []
for item in movieOnly:
	print item
	sharetemp = list(set(item).intersection(inputMovies))
	truMovie.append(sharetemp)
	truMovcount.append(len(sharetemp))



print "user id"
print userOnly
print "Num of shared movies:"
print truMovcount
print "Num of shared tags"
print truNum

friends = []
cursor.execute("select FriendID from UserUser where UserID = %s",(_userID,))
allFriends = cursor.fetchall()
friends.extend([x[0] for x in allFriends])


#dictionary = dict(zip(userOnly, truMovcount))
#print dictionary
dictionary = dict(zip(userOnly, truMovcount))
print dictionary
print "sorted"
import operator
dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse = True)
print dictionary
dictionary = map(list, dictionary)
print dictionary
#print "Recommendation based on Movies"

#print "Recommendation based on Tags"


db.commit()


"""
                        similar = [];
                        occurences = [];
                        for i in range(len(inputMovies)):
                                cursor.execute("SELECT UserId,TitleID FROM UserTitle WHERE TitleID LIKE %s and UserID Not LIKE %s",(inputMovies[i],data[0]))
                                data1 = cursor.fetchall()
                                for item in data1:
                                        temp = [item[0],item[1]]
                                        occurences.append(item[0])
                                        similar.append(temp)
                        #similar = [[5L, 1L], [11L, 1L], [12L, 1L], [3L, 2L], [6L, 2L], [16L, 3L]] form:[UserID, MovieID]
                        #occurences = [5L, 11L, 12L...] these are UserIds

                        #sort occurences so we can list users by best match
                        from collections import Counter
                        bestmatch = sorted(occurences, key=Counter(occurences).get,reverse=True)

                        #remove duplicates while preserving order
                        seen = set()
                        result = []
                        for item in bestmatch:
                                if item not in seen:
                                        seen.add(item)
                                        result.append(item)

                        numofmovies = [0]*len(result)

                        #result is storing best matched users in order, numofmovies is number of shared movies
                        for item in range(len(numofmovies)):
                                numofmovies[item] = bestmatch.count(result[item])

                        #correspond Username with each ID
                        userlist = [];
                        for item in range(len(result)):
                                cursor.execute("SELECT username FROM user WHERE id like %s LIMIT 1",(result[item],))
                                temp = cursor.fetchall()
                                userlist.append(str((temp[0])[0]))

                        final = ', '.join('%s:%s' % t for t in zip(userlist,numofmovies))

                        if len(final) is 0:
                                mysql.connection.commit()
                                return 'No Matches'
                        else:
                                mysql.connection.commit()
                                return final
"""
