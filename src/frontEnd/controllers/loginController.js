//TODO:remove cookie
'use strict'
    var loginApp = angular.module('loginApp', ['ngCookies']);
    loginApp.controller('loginController', function($scope, $location, $window, $cookieStore, $http) {

        //for handling login submit
        $scope.submitLogin = function(){
            var username =$scope.userL.uname;
            var password = $scope.userL.pass;
            var res = $http({
                url: HOST+'accounts/login',
                method: 'POST',
                data: "username=" + username + "&password=" + password,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
            .success(function(data, status, headers, config) {
                //alert('login successfully!' + data.token);
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
                    url: HOST+'accounts/create',
                    method: 'POST',
                    data: "username=" + username + "&password=" + password,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                })
                .success(function(data, status, headers, config) {
                    //alert('register successfully!' + data.token);
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
                 console.log("error in stating or joining a game:" + status);
             });
             
             //$cookieStore.remove('token');
             //alert("remove cookie");
             document.cookie = "token=;path=/";
             console.log("here");
             $window.location.href = document.URL.substr(0,document.URL.lastIndexOf('/')+1)+"../index.html";
    };
    });
