var ngApp = angular.module('myapp', ['ngRoute']);
ngApp.config(
    function($interpolateProvider) {
        $interpolateProvider.startSymbol('{!');
        $interpolateProvider.endSymbol('!}');
        }
);


ngApp.controller('mainCtrl', function($scope, $http, $route) {
	$scope.message = "bottle.py boilerplate";
})
