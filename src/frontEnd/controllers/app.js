var mainApp = angular.module('mainApp', ['ngCookies','mainApp.loginApp','mainApp.chatApp'])
mainApp.config(['$routeProvider',
  function($routeProvider) {
      when('/Home', {
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
      otherwise({
	redirectTo: '/Home'
      });
}]);

mainApp.controller("mainController",function(){});


