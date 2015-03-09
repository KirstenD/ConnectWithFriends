
var friendApp = angular.module("friendApp",['ngCookies']);

friendApp.controller("friendController",function($scope, $cookieStore,$interval ,$http ){
    $scope.names=[{"id":1,"username":"brent"},{"id":2,"username":"matt"},{"id":3,"username":"kevin"}];// dummy variables
    $interval(function(){

    $scope.xmlhttp=new XMLHttpRequest();
    $scope.xmlhttp.open("GET","http://localhost:8000/friends/index",false);//syncronous
    $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
    $scope.xmlhttp.send();
    if ($scope.xmlhttp.status == 200){
         $scope.names  = JSON.parse($scope.xmlhttp.responseText);
         //alert(names[0].id);


    }else{
        alert("exception in index:" + $scope.xmlhttp.responseText);
    }

    $scope.deleteFriend =function(id1){
    $scope.xmlhttp=new XMLHttpRequest();
    $scope.xmlhttp.open("DELETE","http://localhost:8000/friends/delete",false);//syncronous
    $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
    $scope.xmlhttp.send("id=id1");
    if ($scope.xmlhttp.status == 200){
         $scope.n  = JSON.parse($scope.xmlhttp.responseText);
         //alert(names[0].id);


    }else{
        alert("exception in index:" + $scope.xmlhttp.responseText);
    }
    };
       },2000);
});

