
var friendApp = angular.module("friendApp",['ngCookies']);

friendApp.controller("friendController",function($scope, $interval ,$location, $window, $cookieStore, $http ){


    $scope.names=[];// dummy variables
    $interval(function(){

    $scope.xmlhttp=new XMLHttpRequest();
    $scope.xmlhttp.open("GET",HOST+"friends/index",false);//syncronous
    $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
    $scope.xmlhttp.send();
    if ($scope.xmlhttp.status == 200){
         $scope.names  = JSON.parse($scope.xmlhttp.responseText);
         //alert(names[0].id);


    }else{
       console.log("exception in index:" + $scope.xmlhttp.responseText);
    }

    $scope.deleteFriend =function(ids){
        /*
         $scope.xmlhttp=new XMLHttpRequest();
        $scope.xmlhttp.open("DELETE",HOST+"friends/delete",false);//syncronous
        $scope.xmlhttp.setRequestHeader("Authorization","Token "+ $cookieStore.get("token"));
        $scope.xmlhttp.send('id=ids');
        if ($scope.xmlhttp.status == 204){
             $scope.names  = JSON.parse($scope.xmlhttp.responseText);
            //alert(names[0].id);
        }else{
            alert("exception in index:" + $scope.xmlhttp.responseText);
        }
       }*/
       var token = $cookieStore.get("token");
         //alert(token);
         var config = {headers: {
             'Authorization': 'Token '+token,
         }
         };
       $http.delete(HOST+'friends/delete/' + ids, config)
             .success(function( status, headers, config) {
                 console.log('friend Added successfully!');
                 //alert(data.turn);
             })
         .error(function( status, headers, config) {
             console.log("error in addding friend:" + status);
         });
         };

       },2000);
});

