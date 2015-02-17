    var loginApp = angular.module('loginApp', ['ngCookies']);
    loginApp.controller('mainController', function($scope, $location, $window, $cookieStore) {

        //for handling login submit
        $scope.submitLogin = function(){
            //TODO: send request to server, set corresponding cookies
            if ($scope.userL.uname == "guest" && $scope.userL.pass == "guest"){
                alert("login successful!");
                $cookieStore.put('test', 'testcookie');
                $window.location.href = "https://ix.cs.uoregon.edu/~zhuojun/connect4/connect4.html"
            }else{
                alert("login failed!");
            }
        }

        //for handling register submit
        $scope.submitReg = function(){
            alert($scope.usernameReg);
            //TODO: send request to server
        }
    });
