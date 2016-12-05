var movrControllers = angular.module('movrControllers', []);

movrControllers.controller('IndexController', ['$scope', '$location', 'AuthService', function($scope, $location, AuthService) {
    $scope.loggedin = false;
    $scope.$on('login-changed', function(mevent, value) {
        $scope.loggedin = value;
        $location.path('/');
    });
    $scope.logout = function() {
        AuthService.logout();
    }
}]);

movrControllers.controller('SignupController', ['$scope', 'AuthService', function($scope, AuthService) {
    $scope.username = "";
    $scope.password = "";
    $scope.firstname = "";
    $scope.lastname = "";
    $scope.picurl = "";
    
    $scope.signup = function() {
        AuthService.register(
            $scope.username,
            $scope.password,
            $scope.firstname,
            $scope.lastname,
            $scope.picurl
        ).then(function() {
            console.log('Registration success');
        }).catch(function(message) {
            console.log('Error: ' + message);
        });
    };
}]);

movrControllers.controller('LoginController', ['$scope', 'AuthService', function($scope, AuthService) {
    $scope.username = "";
    $scope.password = "";
    $scope.message = "";
    
    $scope.login = function() {
        AuthService.login($scope.username, $scope.password).then(function() {
            console.log('Login success!');
        }).catch(function(message) {
            $scope.message = message;
            console.log('Error: ' + message);
        });
    };
}]);

movrControllers.controller('UserPageController', ['$scope', 'AuthService', 'UserService', 'MovieService', function($scope, AuthService, UserService, MovieService) {
    $scope.user = null;
    $scope.movies = null;
    
    AuthService.getUser().then(function(userdata) {
        MovieService.getMoviesForUser(userdata.username).then(function(moviedata) {
            var ret = [];
            moviedata.forEach(function(arrayElem) {
                var movie = arrayElem;
                MovieService.getKeywordsForMovie(movie[1]).then(function(keywdata) {
                    arrayElem.push(keywdata);
                    ret.push(arrayElem);
                }).catch(function(message) {
                    console.log(message);
                });
            });
            $scope.movies = ret;
        }).catch(function(message) {
            console.log('MESSAGE ' + message);
        });
        
        UserService.getUser(userdata.username).then(function(data) {
            $scope.user = data;
        }).catch(function(message) {
            console.log('Error: ' + message);
        });
    }).catch(function() {
        console.log('not logged in');
    });
    
    MovieService.getMoviesWithTitle('Inception').then(function(data) {
        //console.log(data);
    }).catch(function(message) {
        console.log('Error: ' + message);
    });
}]);

movrControllers.controller('MovieDetailsController', ['$scope', 'MovieService', '$routeParams', function($scope, MovieService, $routeParams) {
    MovieService.getMovieWithID($routeParams.movie_id).then(function(moviedata) {
        $scope.movie = moviedata[0];
        MovieService.getKeywordsForMovie(moviedata[0][0]).then(function(keywdata) {
            $scope.keywords = keywdata;
        }).catch(function(message) {
            
        });
    }).catch(function(message) {
        console.log(message);
    });
}]);

movrControllers.controller('AddMovieController', ['$scope', 'AuthService', 'UserService', 'MovieService', function($scope, AuthService, UserService, MovieService) {
    $scope.title = "";
    $scope.message = "";
    $scope.getMovies = function() {
        MovieService.getMoviesWithTitle($scope.title).then(function(moviedata) {
            $scope.message = "";
            $scope.movies = moviedata;
        }).catch(function(message) {
            $scope.message = message;
            $scope.movies = {};
            console.log('Error: ' + message);
        });
    };
    $scope.addMovie = function(movie_id) {
        AuthService.getUser().then(function(user) {
            UserService.getUser(user.username).then(function(userf) {
                UserService.addFavMovieForUser(userf.id, movie_id).then(function() {
                    $scope.message = "";
                    console.log('Added!');
                }).catch(function(message) {
                    $scope.message = message;
                    console.log(message);
                });
            }).catch(function(message) {
                $scope.message = message;
                console.log('Error: ' + message);
            });
        }).catch(function(message) {
            $scope.message = message;
            console.log('Error: ' + message);
        });
    };
    
    AuthService.getUser().then(function(userdata) {
        UserService.getUser(userdata.username).then(function(data) {
            $scope.user = data;
        }).catch(function(message) {
            console.log('Error: ' + message);
        });
    }).catch(function() {
        console.log('not logged in');
    });
}]);




