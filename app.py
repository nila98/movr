from flask import Flask, render_template, redirect, url_for, request, json, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'main'
app.config['MYSQL_HOST'] = '127.0.0.1'

mysql = MySQL(app)


#mysql.init_app(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	cursor = mysql.connection.cursor()
	try:
		_username = request.json['inputUsername']
		_password = request.json['inputPassword']
		
		cursor.callproc('validateLogin', (_username,))
		data = cursor.fetchall()
		if len(data) is 0:
			return jsonify({
				'result': 'false',
				'message': 'User not found'
			})
		else:
			if data[0][0] == _password:
				return jsonify({
					'result': 'true',
					'message': 'Success',
					'data': {
						'username': _username
					}
				})
			else:
				return jsonify({
					'result': 'false',
					'message': 'Incorrect password'
				})
	except Exception as e:
		return jsonify({
			'result': 'false',
			'message': str(e)
		})
	finally:
		cursor.close()
			
	

@app.route('/signup', methods=['POST'])
def signup():
	cursor = mysql.connection.cursor()
	try:
		_username = request.json['username']
		_password = request.json['password']
		_firstname = request.args.get('firstname')
		_lastname = request.args.get('lastname')
		_picurl = request.args.get('picurl')
		
		cursor.callproc('createUser', (_username, _firstname, _lastname, _password, _picurl))
		data = cursor.fetchall()
		
		if len(data) is 0:
			mysql.connection.commit()
			return jsonify({
				'result': 'true'
			})
		else:
			return jsonify({
				'result': 'false',
				'message': data[0]
			})
	except Exception as e:
		return jsonify({
			'result': 'false',
			'message': str(e)
		})
	finally:
		cursor.close()

@app.route('/getuser', methods=['POST'])
def getuser():
	username = request.json['username']
	cursor = mysql.connection.cursor()
	try:
		cursor.callproc('getUser', (username,))
		data = cursor.fetchall()
		if len(data) is 0:
			return jsonify({'result': 'false', 'message': 'User not found'})
		else:
			return jsonify(data=data, result='true')
	except Exception as e:
		return jsonify({'result': 'false', 'message': str(e)})
	finally:
		cursor.close()

@app.route('/getmovieswithtitle', methods=['POST'])
def getmovie():
	title = request.json['title']
	cursor = mysql.connection.cursor()
	try:
		cursor.callproc('getMoviesWithTitle', (title,))
		data = cursor.fetchall()
		if len(data) is 0:
			return jsonify({'result': 'false', 'message': 'No movies found'})
		else:
			return jsonify(data=data, result='true')
	except Exception as e:
		return jsonify({'result': 'false', 'message': str(e)})
	finally:
		cursor.close()

@app.route('/getmoviesforuser', methods=['POST'])
def getmoviesforuser():
	_username = request.json['username']
	cursor = mysql.connection.cursor()
	try:
		cursor.callproc('getMoviesForUser', (_username,))
		data = cursor.fetchall()
		return jsonify(data=data, result='true')
	except Exception as e:
		return jsonify({'result': 'false', 'message': str(e)})
	finally:
		cursor.close()

@app.route('/addfavmovieforuser', methods=['POST'])
def addfavmovieforuser():
	user_id = request.json['user_id']
	movie_id = request.json['movie_id']
	cursor = mysql.connection.cursor()
	try:
		cursor.callproc('addFavMovieForUser', (user_id, movie_id))
		data = cursor.fetchall()
		if len(data) is 0:
			mysql.connection.commit()
			return jsonify({
				'result': 'true'
			})
		else:
			return jsonify({
				'result': 'false',
				'message': data[0]
			})
	except Exception as e:
		return jsonify({'result': 'false', 'message': str(e)})
	finally:
		cursor.close()

@app.route('/getkeywordsformovie', methods=['POST'])
def getkeywordsformovie():
	movie_id = request.json['movie_id']
	cursor = mysql.connection.cursor()
	try:
		cursor.callproc('getKeywordsForMovie', (movie_id,))
		data = cursor.fetchall()
		if len(data) is 0:
			return jsonify({
				'result': 'false',
				'message': 'No keywords found'
			})
		else:
			return jsonify(data=data, result='true')
	except Exception as e:
		return jsonify({'result': 'false', 'message': str(e)})
	finally:
		cursor.close()

@app.route('/getmoviewithid', methods=['POST'])
def getmoviewithid():
	movie_id = request.json['movie_id']
	cursor = mysql.connection.cursor()
	try:
		cursor.callproc('getMovieWithID', (movie_id,))
		data = cursor.fetchall()
		if len(data) is 0:
			return jsonify({
				'result': 'false',
				'message': 'Not found'
			})
		else:
			return jsonify(data=data, result='true')
	except Exception as e:
		return jsonify({'result': 'false', 'message': str(e)})
	finally:
		cursor.close()

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
        if request.method == 'GET':
                return render_template('add_movie.html')

        cursor = mysql.connection.cursor()
        print "connected to db"
        try:
                _userID = request.form['inputUserID']
                _searchMovie = request.form['inputMovie']

                if _userID and _searchMovie:
			cursor.execute("SELECT id FROM title WHERE title like %s LIMIT 1", (_searchMovie,))

			data = cursor.fetchall()
			if len(data) is 0:
				mysql.connection.commit()
				return 'movie not found'

                        cursor.execute("""INSERT INTO UserTitle VALUES(%s,%s)""", (_userID, data[0]))
			data = cursor.fetchall()

                        if len(data) is 0:
                                mysql.connection.commit()
                                return 'success'
                        else:
                                return 'error in insert for UserTitle'
                else:
                        return 'Please enter the required fields'
        except Exception as e:
                return e
        finally:
                cursor.close()



@app.route('/commonmovie', methods=['GET', 'POST'])
def commonmovie():
        if request.method == 'GET':
                return render_template('commonmovie.html')

        cursor = mysql.connection.cursor()
        print "connected to db"
        try:
                _user1 = request.form['username1']
                _user2 = request.form['username2']

                if _user1 and _user2:
                        cursor.execute("SELECT id FROM user WHERE username like %s LIMIT 1", (_user1,))
                        data = cursor.fetchall()
                        if len(data) is 0:
                                mysql.connection.commit()
                                return 'first username not found'

                        cursor.execute("SELECT id FROM user WHERE username like %s LIMIT 1", (_user2,))
                        data2 = cursor.fetchall()
                        if len(data2) is 0:
                                mysql.connection.commit()
                                return 'second username not found'

			
                        cursor.execute("SELECT TitleID FROM UserTitle where UserID = %s", (data[0],))
                        movielist1 = cursor.fetchall()
                        cursor.execute("SELECT TitleID FROM UserTitle where UserID = %s", (data2[0],))
                        movielist2 = cursor.fetchall()
			movielist1 = [item[0] for item in movielist1]
			movielist2 = [item[0] for item in movielist2]
			#cursor.execute('select user1.UserID, user2.UserID, user1.TitleID from UserTitle user1 inner join UserTitle user2 on user1.TitleID = user2.TitleID and user1.UserID = %s and user2.UserID = %s', (data[0], data2[0]))
			#commonlist = [item[0] for item in cursor.fetchall()]
			#map(list, commonlist)
			commonlist = list(set(movielist1) & set(movielist2))
			finallist = [];
			for i in range(len(commonlist)):
				cursor.execute("SELECT title FROM title WHERE id = %s LIMIT 1",(commonlist[i],))
				finallist.append(((cursor.fetchall())[0])[0])
			
                        if len(finallist) is 0:
                                return 'no similar movies'
                        else:
				mysql.connection.commit()
				return ", ".join(finallist)
                else:
                        return 'Please enter the required fields'
        except Exception as e:
                return e
        finally:
                cursor.close()


@app.route('/findsim', methods=['GET', 'POST'])
def findsim():
        if request.method == 'GET':
                return render_template('findsim.html')

        cursor = mysql.connection.cursor()
        print "connected to db"
        try:
		# although it says ID, it's actually the username
                _userID = request.form['inputUserID']

                if _userID:
                        cursor.execute("SELECT id FROM user WHERE username like %s LIMIT 1", (_userID,))
                        data = cursor.fetchall()
                        if len(data) is 0:
                                mysql.connection.commit()
                                return 'unknown username'

			cursor.execute("SELECT TitleID FROM UserTitle WHERE UserID like %s",(data[0],))

                        data = cursor.fetchall()#data = ((1L,), (2L,), (7L,)) type:tuples
                        inputMovies = [item[0] for item in data]#inputMovies = [1L,2L,7L] type:list

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
                else:
                        return 'Please enter the required fields'
        except Exception as e:
                return e
        finally:
                cursor.close()




@app.route('/matches')
def matches():
	return render_template('matches.html')

@app.route('/recommendations')
def recommendations():
	return render_template('recommendations.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
