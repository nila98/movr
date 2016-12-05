var app = angular.module('movr', ['ngRoute', 'movrControllers', 'movrServices']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/', {
        templateUrl: '/static/partials/index.html',
    }).
    when('/login', {
        templateUrl: '/static/partials/login.html',
        controller: 'LoginController'
    }).
    when('/userpage', {
        templateUrl: '/static/partials/userpage.html',
        controller: 'UserPageController'
    }).
    when('/signup', {
        templateUrl: '/static/partials/signup.html',
        controller: 'SignupController'
    }).
    when('/addmovie', {
        templateUrl: '/static/partials/addmovie.html',
        controller: 'AddMovieController'
    }).
    when('/moviedetails/:movie_id', {
        templateUrl: '/static/partials/moviedetails.html',
        controller: 'MovieDetailsController'
    }).
    otherwise({
        redirectTo: '/'
    });
}]);


