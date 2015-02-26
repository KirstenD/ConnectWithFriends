   'use strict'
var chatApp = angular.module('chatApp', ['ngCookies','Luegg.directives']);
chatApp.controller('chatController', function($scope, $interval) {
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

});

