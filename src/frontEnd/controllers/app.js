   'use strict'
var mainApp = angular.module('mainApp', ["ngRoute",'ngCookies',"loginApp","chatApp","gameApp","friendApp","gameChatApp"])
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
      when("/friend",{
      templateUrl: "../html/friend.html",
      controller: "friendController"
      }).
      when("/gameChat",{
      templateUrl: "../html/gameChat.html",
      controller: "gameChatController"
      }).
      otherwise({
	redirectTo: '/Home'
      });
}]);

mainApp.controller("mainController",function($scope, $window, $cookieStore, $http){
     document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"friend.html";

    $scope.xmlhttp=new XMLHttpRequest();
    $scope.xmlhttp.open("GET",HOST+"accounts/whoami",false);
    $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
    $scope.xmlhttp.send();
    if ($scope.xmlhttp.status == 200){
         $scope.user  = JSON.parse($scope.xmlhttp.responseText);
        //alert(game.id);


    }else{
        alert("exception in whoami:" + $scope.xmlhttp.responseText)
    }


});

