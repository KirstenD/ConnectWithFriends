//TODO: error handling
   'use strict'
var gameApp = angular.module('gameApp', ['ngCookies']);
gameApp.controller('gameController', function($scope, $interval ,$location, $window, $cookieStore, $http) {

     $scope.game = function(){

         document.getElementById("iframe").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"game.html";

         var token = $cookieStore.get("token");
         //alert(token);
         var config = {headers: {
             'Authorization': 'Token '+token,
         }
         };
         $http.post('http://localhost:8000/games/start',
             {text:$scope.msg},
             config
             )
             .success(function(data, status, headers, config) {
                 //alert('message sent successfully!');
                 alert(data.turn);
             })
         .error(function(data, status, headers, config) {
             alert(data.detail);
         });

    };
});

