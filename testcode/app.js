function login($scope, $location){
			//var $promise=$http.post('data/user.php',data); //send data to user.php
			//$promise.then(function(msg){
				var uid = 1;
				//var uid=msg.data;
				if(uid==0){
					//scope.msgtxt='Correct information';
					//sessionService.set('uid',uid);
					$location.path('/home');
				}
				else  {
					//scope.message='incorrect information';
                    $location.path("/chat")
				}

		};
var sampleApp = angular.module('sampleApp', []);

sampleApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/Login', {
	templateUrl: 'login.html',
	controller: 'LoginController'
      }).
      when('/Home', {
	templateUrl: 'home.html',
	controller: 'HomeController'
      }).
      when('/chat', {
	templateUrl: 'chat.html',
	controller: 'chatController'
      }).
      otherwise({
	redirectTo: '/Login'
      });
}]);


sampleApp.controller('LoginController', function($scope,$location) {

	$scope.message = 'This is Login screen';
    login($scope,$location);

});


sampleApp.controller('HomeController', function($scope) {

	$scope.message = 'This is home screen';

});
sampleApp.controller('chatController', function($scope) {

	$scope.message = 'This is chat screen';

});