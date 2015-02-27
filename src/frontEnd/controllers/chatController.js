   'use strict'
var chatApp = angular.module('chatApp', ['ngCookies','luegg.directives']);
chatApp.controller('chatController', function($scope, $interval ,$location, $window, $cookieStore, $http) {
    $scope.global_msgs=[];
    $scope.names=['Jani','Hege','Kai'];
    $interval(function(){
        var token = $cookieStore.get("token");
        var config = {headers: {
            'Authorization': 'Token '+token,
        }
        };

        $http.get('http://localhost:8000/chat/index' , config)
        .success(function(data, status, headers, config) {
            $scope.global_msgs = data;
            //alert(angular.toJson(data));
            //alert('message received successfully!');
        })
        .error(function(data, status, headers, config) {
            alert(data.detail);
        });
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
        var token = $cookieStore.get("token");
        //alert($scope.msg+token);

        var config = {headers: {
            'Authorization': 'Token '+token,
        }
        };

        $http.post('http://localhost:8000/chat/send',
            {text:$scope.msg},
            config
        )
        .success(function(data, status, headers, config) {
            //alert('message sent successfully!');
        })
        .error(function(data, status, headers, config) {
            alert(data.detail);
        });

        $scope.msg = null;  //clear the input form
    };
     $scope.chat = function(){
        //alert("chating is fun");
        //alert($cookieStore.get("token"));
       document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"chat.html";
    };
});

