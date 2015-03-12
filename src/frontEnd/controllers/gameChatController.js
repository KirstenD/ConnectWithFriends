
var chatApp = angular.module('gameChatApp', ['ngCookies','luegg.directives']);

chatApp.controller('gameChatController', function($scope, $interval ,$location, $window, $cookieStore, $http) {
    $scope.global_msgs=[];
    $scope.friends =[];
  // $scope.names=[{"id":1,"username":"brent"},{"id":2,"username":"matt"},{"id":3,"username":"kevin"}];

    $interval(function(){
        var token = $cookieStore.get("token");
        var config = {headers: {
            'Authorization': 'Token '+token,
        }
        };

        $http.get(HOST+'chat/game/index' , config)
        .success(function(data, status, headers, config) {
            $scope.global_msgs = data;
            //alert(angular.toJson(data));
            //alert('message received successfully!');
        })
        .error(function(data, status, headers, config) {
            //[-]alert(data.detail);
        });
        $http.get(HOST + "accounts/index",config).success(function(data,status,headers,config){
            $scope.name = data;
           })
           .error(function(data,status,header,config){
            //alert(data.detail);
           });

    },2000);


    $scope.send = function(){
        var token = $cookieStore.get("token");
        //alert($scope.msg+token);

        var config = {headers: {
            'Authorization': 'Token '+token,
        }
        };

        $http.post(HOST+'chat/game/send',
            {text:$scope.msg},
            config
        )
        .success(function(data, status, headers, config) {
            //alert('message sent successfully!');
        })
        .error(function(data, status, headers, config) {
            console.log(data);
        });

        $scope.msg = null;  //clear the input form
    };
});

