var movrServices = angular.module('movrServices', []);

movrServices.factory('AuthService', function($q, $timeout, $http, $rootScope) {
    var user = null;
    return {
    
    login: function(username, password) {
        var deferred = $q.defer();
        
        $http.post('/login', {inputUsername: username, inputPassword: password})
        .success(function(data) {
            if (data.result == 'true') {
                user = data.data;
                $rootScope.$broadcast('login-changed', true);
                deferred.resolve();
            } else {
                //user = null;
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    logout: function() {
        if (user != null) {
            user = null;
            $rootScope.$broadcast('login-changed', false);
        }
    },
    getUser: function() {
        var deferred = $q.defer();
        if (user == null) {
            deferred.reject('Not logged in');
        } else {
            deferred.resolve(user);
        }
        return deferred.promise;
    },
    register: function(username, password, firstname, lastname, picture) {
        var deferred = $q.defer();
        
        $http.post('/signup', {
            username: username,
            password: password,
            firstname: firstname,
            lastname: lastname,
            picture: picture
        }).success(function(data) {
            if (data.result == 'true') {
                deferred.resolve();
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    }
    
    }
});

movrServices.factory('UserService', function($q, $http, $rootScope) {
    return {
    getUser: function(username) {
        var deferred = $q.defer();
        
        $http.post('/getuser', {username: username})
        .success(function(data) {
            if (data.result == 'true') {
                var user = data.data;
                var ret = {
                    id: user[0][0],
                    username: user[0][1],
                    password: user[0][2],
                    firstname: user[0][3],
                    lastname: user[0][4],
                    picture: user[0][5]
                };
                deferred.resolve(ret);
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    addFavMovieForUser: function(user_id, movie_id) {
        var deferred = $q.defer();
        
        $http.post('/addfavmovieforuser', {user_id: user_id, movie_id: movie_id})
        .success(function(data) {
            if (data.result == 'true') {
                deferred.resolve();
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    }
});

movrServices.factory('MovieService', function($q, $http, $rootScope) {
    return {
    getMovie: function(movie_id) {
        
    },
    getMoviesWithTitle: function(title) {
        var deferred = $q.defer();
        
        $http.post('/getmovieswithtitle', {title: title})
        .success(function(data) {
            if (data.result == 'true') {
                deferred.resolve(data.data);
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    getMoviesForUser: function(username) {
        var deferred = $q.defer();
        
        $http.post('/getmoviesforuser', {username: username})
        .success(function(data) {
            if (data.result == 'true') {
                deferred.resolve(data.data);
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    getRecommendedMovie(movie_id, user_id) {
        // get all keywords of a user's UserTitle
        // parse keywords into dictionary, with frequency as keys
        // select a movie according to formula:
        // weighted intersection / weighted union, where items not in the dictionary are weighted as 1.
        // choose movie that has highest value

        var deferred = $q.defer();
        $http.post('/getleftjaccardvalue', {movie_id: movie_id, user_id: user_id})
        .success(function(data) {
            if (data.result = 'true') {
                console.log('jaccard val');
                console.log(data);
                deferred.resolve(data.data);
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    getKeywordsForMovie(movie_id) {
        var deferred = $q.defer();
        $http.post('/getkeywordsformovie', {movie_id: movie_id})
        .success(function(data) {
            if (data.result = 'true') {
                deferred.resolve(data.data);
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    },
    getMovieWithID(movie_id) {
        var deferred = $q.defer();
        $http.post('/getmoviewithid', {movie_id: movie_id})
        .success(function(data) {
            if (data.result = 'true') {
                deferred.resolve(data.data);
            } else {
                deferred.reject(data.message);
            }
        }).error(function(data) {
            deferred.reject(data.message);
        });
        return deferred.promise;
    }
    }
});




