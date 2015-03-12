//TODO: error handling
   'use strict'
var gameApp = angular.module('gameApp', ['ngCookies']);
gameApp.controller('gameController', function($scope, $interval ,$location, $window, $cookieStore, $http) {

     $scope.game = function(){

         //delete then append, so the history will not be recorded
         var ifr = document.getElementById("iframe");
         ifr.parentNode.removeChild(ifr);
         var ifr2 = document.getElementById("iframe2");
         ifr2.parentNode.removeChild(ifr2);

         ifr = document.createElement('iframe');
         ifr.width = "800";
         ifr.height = "500";
         ifr.id = "iframe";
         ifr.class = "iframe1";
         ifr.src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"game.html";;
         ifr2 = document.createElement('iframe');
         ifr2.width = "400";
         ifr2.height = "500";
         ifr2.id = "iframe2";
         ifr2.src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"gameChat.html";
         document.body.appendChild(ifr);
         document.body.appendChild(ifr2);

         //document.getElementById("iframe").width="800";
         //document.getElementById("iframe2").width = "400";
         //document.getElementById("iframe").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"game.html";
         //document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"gameChat.html";
         var token = $cookieStore.get("token");
         //alert(token);
         var config = {headers: {
             'Authorization': 'Token '+token,
         }
         };
         $http.post(HOST+'games/forfeit',
             null,
             config
             )
             .success(function(data, status, headers, config) {
                 console.log('message sent successfully!');
                 //alert(data.turn);
             })
         .error(function(data, status, headers, config) {
             console.log("error in forfeiting a game:" + status);
         });
         $http.post(HOST+'games/start',
             null,
             config
             )
             .success(function(data, status, headers, config) {
                 //alert('message sent successfully!');
                 //alert(data.turn);
             })
         .error(function(data, status, headers, config) {
             //alert("error in stating or joining a game:" + status);
             console.log("error in stating or joining a game:" + status);
         });

    };
});
