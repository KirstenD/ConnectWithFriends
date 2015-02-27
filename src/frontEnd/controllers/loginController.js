'use strict'
    var loginApp = angular.module('loginApp', ['ngCookies']);
    loginApp.controller('loginController', function($scope, $location, $window, $cookieStore, $http) {

        //for handling login submit
        $scope.submitLogin = function(){
            var username =$scope.userL.uname;
            var password = $scope.userL.pass;
            var res = $http({
                url: 'http://localhost:8000/accounts/login',
                method: 'POST',
                data: "username=" + username + "&password=" + password,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
            .success(function(data, status, headers, config) {
                alert('login successfully!' + data.token);
                $cookieStore.put('token', data.token);
                $window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"html/main.html";
            })
            .error(function(data, status, headers, config) {
                alert( "login fail: " + data);
            });
        }

        //for handling register submit
        $scope.submitReg = function(){
            //alert($scope.userR.uname);
            if ($scope.userR.pass1 != $scope.userR.pass2){
                alert("2 passwords are not the same!");
            }else{
                var username = $scope.userR.uname;
                var password = $scope.userR.pass1;
                var res = $http({
                    url: 'http://localhost:8000/accounts/create',
                    method: 'POST',
                    data: "username=" + username + "&password=" + password,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                })
                .success(function(data, status, headers, config) {
                    alert('register successfully!' + data.token);
                    $cookieStore.put('token', data.token);
                    $window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"html/main.html";
                })
                .error(function(data, status, headers, config) {
                    if (status == 409){
                    alert("user already exsits!");
                    }else{
                        alert( "failure message: " + JSON.stringify({data: data}));
                    }
                });
            }
        }
         $scope.logout = function(){
        alert("destroy token");
        $window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"../index.html";
    };
    });
