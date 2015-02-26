'use strict'
    var loginApp = angular.module('loginApp', ['ngCookies']);
    loginApp.controller('loginController', function($scope, $location, $window, $cookieStore, $http) {

        //for handling login submit
        $scope.submitLogin = function(){
            //TODO: send request to server, set corresponding cookies
            if ($scope.userL.uname == "guest" && $scope.userL.pass == "guest"){
                alert("login successful!");

                //send request to django server and store cookie if successful
                $http.get('http://www.w3schools.com/website/Customers_JSON.php').
                  success(function(data, status, headers, config) {
                      alert(data);
                      $cookieStore.put('test', 'testcookie');
                      $window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"../index.html";
                  }).
                  error(function(data, status, headers, config) {
                      alert(status);
                  });
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
