var ngApp = angular.module('myapp', ['ngRoute']);


ngApp.controller('mainCtrl', function($scope, $http, $route) {
	$scope.message = "bottle.py boilerplate";
})
