var connect4App = angular.module('connect4App',[]);
connect4App.controller('connect4Controller', ['$scope', '$interval', function($scope, $interval) {
    $scope.names=['Jani','Hege','Kai'];
    $interval(function(){
        //alert($scope.names);
        $scope.names[$scope.names.length] = $scope.names[$scope.names.length-1] + 'z';
    },2000);
}]);