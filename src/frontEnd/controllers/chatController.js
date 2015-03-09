
var chatApp = angular.module('chatApp', ['ngCookies','luegg.directives']);

chatApp.controller('chatController', function($scope, $interval ,$location, $window, $cookieStore, $http) {
    $scope.global_msgs=[];
    $scope.friends =[];
  // $scope.names=[{"id":1,"username":"brent"},{"id":2,"username":"matt"},{"id":3,"username":"kevin"}];

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
            //[-]alert(data.detail);
        });
        $http.get("http://localhost:8000/accounts/index",config).success(function(data,status,headers,config){
            $scope.name = data;
           })
           .error(function(data,status,header,config){
            //alert(data.detail);
           });

    },2000);

     $scope.addFriend = function(id1){

        $scope.xmlhttp=new XMLHttpRequest();
        $scope.xmlhttp.open("POST","http://localhost:8000/friends/index",false);//syncronous
        $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
        $scope.xmlhttp.send("id=id1");
        if ($scope.xmlhttp.status == 200){
             $scope.names  = JSON.parse($scope.xmlhttp.responseText);
            //alert(names[0].id);


        }else{
            alert("exception in index:" + $scope.xmlhttp.responseText)
        }

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
        document.getElementById("iframe").width="1000"
        document.getElementById("iframe2").width = "200";
       document.getElementById("iframe").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"chat.html";
       document.getElementById("iframe2").src = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"friend.html";
    };
});

