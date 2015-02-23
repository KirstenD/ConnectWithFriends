var mainApp = angular.module('mainApp', ['ngCookies','mainApp.loginApp','mainApp.chatApp'])
mainApp.config(['$routeProvider',
  function($routeProvider) {
      when('/Home', {
	templateUrl: '../html/index.html',
	controller: 'mainController'
      }).
      when('/chat', {
	templateUrl: '../html/chat.html',
	controller: 'chat2Controller'
      }).
      when('/logout', {
	templateUrl: '../html/login.html',
	controller: 'logoutController'
      }).
      otherwise({
	redirectTo: '/Home'
      });
}]);

mainApp.controller("mainController",function(){});


mainApp.controller('logoutController', function($scope ,$location, $window ) {
$scope.logout = function(){
$window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"html/login.html";
//alert("logout");

};
});

mainApp.controller('chat2Controller', function($scope ,$location, $window ) {
$scope.chat = function(){
$window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"html/chat.html";
//alert("chatting ");

};
});