   'use strict'
var chatApp = angular.module('chatApp', ['ngCookies','luegg.directives']);
chatApp.controller('chatController', function($scope, $interval ,$location, $window, $cookieStore, $http) {
    $scope.names=['Jani','Hege','Kai'];
    $interval(function(){
        //alert($scope.names);
        $scope.names[$scope.names.length] = $scope.names[$scope.names.length-1] + 'z';
    },2000);


     $scope.addFriend = function(name){
        alert("add "+name);
    };
    $scope.chat = function(name){
        alert("chat "+name);
    };
    $scope.challenge = function(name){
        alert("challenge "+name);
    };
    $scope.send = function(){
        alert($scope.msg);
    };
     $scope.chat = function(){
        alert("chating is fun");
       document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"html/chat.html";
    };

});

