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

    self.findApp = function(appId) {
      var app;
      $.each(self.apps, function(idx, item) {
        if (item.key == appId) {
          app = item;
          return false;
        }
      });
      return app;
    };

    self.findAndSelectApp = function(appId) {
      var app = self.findApp(appId);
      self.selectApp(app);
      return app;
    };

    self.apps = App.query(function() {
      // preselect first
      self.selectApp(self.apps[0]);
    });

    $rootScope.appState = self;
  });

var consoleApp = angular.module('console', ["console.services"]).
  config(function($routeProvider) {
     $routeProvider.
        when('/:appID/details', { controller: "AppDetailsCtrl",
            templateUrl: "/static/tmpl/details.tmpl"}).
        when('/:appID/dashboard', { controller: "DashboardCtrl",
            templateUrl: "/static/tmpl/details.tmpl"}).
//       when('/', {controller:MainCtrl, templateUrl:'main.html'}).
// //      when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
// //      when('/new', {controller:CreateCtrl, templateUrl:'detail.html'}).
      otherwise({redirectTo:'/'});
  }).
  controller ("NavbarCtrl", function($scope, appState){
    $scope.appState = appState;

  }).
  controller ("DashboardCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.name = app.name;
    $scope.key = app.key;
    $scope.secret = app.secret;
  }).
  controller ("AppDetailsCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.name = app.name;
    $scope.key = app.key;
    $scope.secret = app.secret;
  }).
  controller ("AddAppCtrl", function ($scope, $location, App, appState) {
    $scope.model = {};

    $scope.saveApp = function() {
      var newApp = new App({name: $scope.model.app_name});
      $scope.model.app_name = null;
      newApp.$save(function() {

        appState.addApp(newApp);
        $scope.dismiss();
        $location.path("/" +  newApp.key + "details/");
      });
    };
  });