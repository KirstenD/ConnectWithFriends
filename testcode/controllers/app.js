var mainApp = angular.module('mainApp', ["ngRoute",'ngCookies','mainApp.loginApp','mainApp.chatApp'])
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

mainApp.controller("mainController",function($scope,$routeProvider){
    $scope.chaturl = "../html/chat.html";
    $scope.frame = "iframe";
    $scope.setURLChat = function(){

        document.getElementById($scope.frame).src =$scope.chaturl ;
};


});

