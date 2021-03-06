'use strict'
var chatApp = angular.module('chatApp', ['ngCookies','luegg.directives']);

chatApp.controller('chatController', function($scope, $interval ,$location, $window, $cookieStore, $http) {
    $scope.global_msgs=[];
    $scope.friends =[];
  // $scope.names=[{}];
    $interval(function(){
        var token = $cookieStore.get("token");
        var config = {headers: {
            'Authorization': 'Token '+token,
        }
        };

        $http.get(HOST+'chat/index' , config)
            .success(function(data, status, headers, config) {
                $scope.global_msgs = data;
                //alert(angular.toJson(data));
                //alert('message received successfully!');
        })
        .error(function(data, status, headers, config) {
            //[-]alert(data.detail);
        });
       $scope.xmlhttp=new XMLHttpRequest();
        $scope.xmlhttp.open("GET",HOST+"accounts/index",false);//syncronous
        $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
        $scope.xmlhttp.send();
        if ($scope.xmlhttp.status == 200){
             $scope.names  = JSON.parse($scope.xmlhttp.responseText);
            //alert(names[0].id);


        }else{
            console.log("exception in index:" + $scope.xmlhttp.responseText)
        }

    },2000);
     
     $scope.addFriend = function(id1){

        var token = $cookieStore.get("token");
         //alert(token);
         var config = {headers: {
             'Authorization': 'Token '+token,
         }
         };
         $http.post(HOST+'friends/add',
            {"id": id1},
             config
             )
             .success(function(data, status, headers, config) {
                 console.log('friend Added successfully!');
                 //alert(data.turn);
             })
         .error(function(data, status, headers, config) {
             console.log("error in addding friend:" + status);
         });
         };
    //$scope.chat = function(name){
    //    alert("chat "+name);
    //};
    //$scope.challenge = function(name){
    //    alert("challenge "+name);
    //};
    $scope.send = function(){
        var token = $cookieStore.get("token");
        //alert($scope.msg+token);

        var config = {headers: {
            'Authorization': 'Token '+token,
        }
        };

        $http.post(HOST+'chat/send',
            {text:$scope.msg},
            config
        )
        .success(function(data, status, headers, config) {
            //alert('message sent successfully!');
        })
        .error(function(data, status, headers, config) {
           console.log(data.detail);
        });

        $scope.msg = null;  //clear the input form
    };
     $scope.chat = function(){
        //alert("chating is fun");
        //alert($cookieStore.get("token"));

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

         //delete then append, so the history will not be recorded
         var ifr = document.getElementById("iframe");
         ifr.parentNode.removeChild(ifr);
         var ifr2 = document.getElementById("iframe2");
         ifr2.parentNode.removeChild(ifr2);

         ifr = document.createElement('iframe');
         ifr.width = "1000";
         ifr.height = "500";
         ifr.id = "iframe";
         ifr.class = "iframe1";
         ifr.src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"chat.html";;
         ifr2 = document.createElement('iframe');
         ifr2.width = "200";
         ifr2.height = "500";
         ifr2.id = "iframe2";
         ifr2.src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"friend.html";
         document.body.appendChild(ifr);
         document.body.appendChild(ifr2);

         //document.getElementById("iframe").width="1000";
         //document.getElementById("iframe2").width = "200";
         //document.getElementById("iframe").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"chat.html";
         //document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"friend.html";
    };
});

