   'use strict'
var mainApp = angular.module('mainApp', ["ngRoute",'ngCookies',"loginApp","chatApp","gameApp"])
mainApp.config(['$routeProvider',
  function($routeProvider) {
     $routeProvider.when('/Home', {
	templateUrl: '../html/index.html',
	controller: 'mainController'
      }).
      when('/chat', {
	templateUrl: '../html/chat.html',
	controller: 'chatController'
      }).
      when('/logout', {
	templateUrl: '../html/login.html',
	controller: 'loginController'
      }).
      when('/game', {
	templateUrl: '../html/game.html',
	controller: 'gameController'
      }).
      otherwise({
	redirectTo: '/Home'
      });
}]);

mainApp.controller("mainController",function($scope, $window, $cookieStore, $http){

});

