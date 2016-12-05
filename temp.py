import MySQLdb

# connect
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",
db="main")

cursor = db.cursor()

# execute SQL select statement
_userID = 26
cursor.execute("SELECT TitleID FROM UserTitle WHERE UserID = %s",(_userID,))

data = cursor.fetchall()#data = ((1L,), (2L,), (7L,)) type:tuples
inputMovies = [item[0] for item in data]#inputMovies = [1L,2L,7L] type:list

tagList=[]

for item in data:
	cursor.execute("select keyword_id from movie_keyword where movie_id = %s",item)
	tagList.extend(cursor.fetchall())


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

from itertools import groupby
from collections import Counter
countTags = []
for item in sharedTags:
	if item != []:
		#item = item.sort()
		print item
		a = reversed(sorted(item,key=item.count))
		outlist = []
		for element in a:
			if element not in outlist:
				outlist.append(element)
		print a
		countTags.append(outlist)
		#countTags.append([len(list(group)) for key, group in groupby(item)])
	else:
		countTags.append([])
#for x,y in enumerate(countTags):
#	print countTags[y]
#print countTags




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
