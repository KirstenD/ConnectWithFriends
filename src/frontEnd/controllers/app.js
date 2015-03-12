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

    var ifr = document.getElementById("iframe");
    ifr.parentNode.removeChild(ifr);
    var ifr2 = document.getElementById("iframe2");
    ifr2.parentNode.removeChild(ifr2);

    ifr = document.createElement('iframe');
    ifr.width = "1000";
    ifr.height = "500";
    ifr.id = "iframe";
    ifr.src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"chat.html";;
    ifr2 = document.createElement('iframe');
    ifr2.width = "200";
    ifr2.height = "500";
    ifr2.id = "iframe2";
    ifr2.src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"friend.html";
    document.body.appendChild(ifr);
    document.body.appendChild(ifr2);


     //document.getElementById("iframe").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"chat.html";
     //document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"friend.html";

    $scope.xmlhttp=new XMLHttpRequest();
    $scope.xmlhttp.open("GET",HOST+"accounts/whoami",false);
    $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
    $scope.xmlhttp.send();
    if ($scope.xmlhttp.status == 200){
         $scope.user  = JSON.parse($scope.xmlhttp.responseText);
        //alert(game.id);


    }else{
        console.log("exception in whoami:" + $scope.xmlhttp.responseText)
    }


});

