var mainApp = angular.module('mainApp', ["ngRoute",'ngCookies'])
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
	controller: 'mainApp.loginApp.loginController'
      }).
      otherwise({
	redirectTo: '/Home'
      });
}]);

mainApp.controller("mainController",function($scope,$window){
    $scope.chaturl = "../html/chat.html";
    $scope.frame = "iframe";
    $scope.setURLChat = function(){

        document.getElementById($scope.frame).src =$scope.chaturl ;
    };
    $scope.logout = function(){
        alert("destroy token");
        $window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"html/login.html";

    };



});

