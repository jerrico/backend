var consoleServices = angular.module('consoleServices', ['ngResource']).
    factory('Apps', function($resource){
  return $resource('/api/v0/my_apps', {}, {
    query: {method:'GET', params: {"_raw": 1}, isArray:true}
  });
});

var consoleApp = angular.module('console', ["consoleServices"]).
  config(function($routeProvider) {
//    console.log($routeProvider);
//     $routeProvider.
//       when('/', {controller:MainCtrl, templateUrl:'main.html'}).
// //      when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
// //      when('/new', {controller:CreateCtrl, templateUrl:'detail.html'}).
//       otherwise({redirectTo:'/'});
  });
consoleApp.value("appName", "consoleApp");

consoleApp.controller("NavbarCtrl", function($scope, Apps) {
  console.log($scope);
  $scope.apps = Apps.query(function() {
    // preselect first
    $scope.selectApp($scope.apps[0]);
  });
  $scope.selectApp = function(app) {
    $scope.selected_app = app;
    console.log(app);
  };
}).
controller ("AddAppCtrl", function ($scope, Apps) {

  $scope.model = {};

  $scope.saveApp = function() {
    console.log($scope.model.app_name);

  };
  
});