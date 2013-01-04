angular.module('console.services', ['ngResource']).
  factory('App', function($resource){
    return $resource('/api/v0/my_apps', {}, {
      query: {method:'GET', params: {"_raw": 1}, isArray:true},
      save: {method:'POST', params: {"_raw": 1}, isArray:false}
    });
  }).
  directive('twModal', function() {
    return {
      scope: true,
      link: function(scope, element, attr, ctrl) {
          scope.show = function() {
            $(element).modal("show");
          };
          scope.dismiss = function() {
            $(element).modal("hide");
          };
        }
      };
  }).
  service('appState', function(App, $rootScope){
    var self = this;
    self.selected_app = null;

    self.selectApp = function(app) {
      self.selected_app = app;
    };

    self.addApp = function(app) {
      self.apps.push(app);
    };

    self.apps = App.query(function() {
      // preselect first
      self.selectApp(self.apps[0]);
    });
  })
;

var consoleApp = angular.module('console', ["console.services"]).
  config(function($routeProvider) {
//    console.log($routeProvider);
//     $routeProvider.
//       when('/', {controller:MainCtrl, templateUrl:'main.html'}).
// //      when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
// //      when('/new', {controller:CreateCtrl, templateUrl:'detail.html'}).
//       otherwise({redirectTo:'/'});
  }).
  controller ("NavbarCtrl", function($scope, appState){
    $scope.appState = appState;

  }).
  controller ("AddAppCtrl", function ($scope, $location, App, appState) {
    $scope.model = {};
    console.log($scope);

    $scope.saveApp = function() {
      var newApp = new App({name: $scope.model.app_name});
      $scope.model.app_name = null;
      newApp.$save(function() {

        appState.addApp(newApp);
        $scope.dismiss();
        $location.path("/details/" + newApp.key);
      });
    };
  });