angular.module('console.services', ['ngResource']).
  factory('App', function($resource){
    return $resource('/api/v1/my_apps', {}, {
      get: {method:'GET', params: {"_raw": 1}, isArray:false},
      query: {method:'GET', params: {"_raw": 1}, isArray:true},
      save: {method:'POST', params: {"_raw": 1}, isArray:false}
    });
  }).
  factory('LogEntry', function($resource){
    return $resource('/api/v1/logs', {}, {
      get: {method:'GET', params: {"_raw": 1}, isArray:false},
      query: {method:'GET', params: {"_raw": 1}, isArray:true},
      save: {method:'POST', params: {"_raw": 1}, isArray:false}
    });
  }).
  factory('Profile', function($resource){
    return $resource('/api/v1/profiles/:profileID', {profileID:'@id', "_key": "@appKey", "_raw": 1}, {
      get: {method:'GET', params: {}, isArray:false},
      query: {method:'GET', params: {}, isArray:true},
      save: {method:'POST', params: {}, isArray:false}
    });
  }).
  factory('User', function($resource){
    return $resource('/api/v1/users/:userID', {userID:'@id'}, {
      get: {method:'GET', params: {"_raw": 1}, isArray:false},
      query: {method:'GET', params: {"_raw": 1}, isArray:true},
      save: {method:'POST', params: {"_raw": 1}, isArray:false}
    });
  }).
  factory('Device', function($resource){
    return $resource('/api/v1/devices/:deviceID', {deviceID:'@id'}, {
      get: {method:'GET', params: {"_raw": 1}, isArray:false},
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
  service('appState', function(App, Profile, $rootScope){
    var self = this;
    self.selected_app = null;
    self.profiles = null;

    self.selectApp = function(app) {
      if (!app.profiles) app.profiles = Profile.query({_key:app.key});
      self.selected_app = app;
      self.profiles = app.profiles;
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

        when('/:appID/devices/:deviceID', { controller: "DeviceDetailsCtrl",
            templateUrl: "/static/tmpl/device_details.tmpl"}).

        // listings
        when('/:appID/logs', { controller: "ListCtrl",
            templateUrl: "/static/tmpl/logs.tmpl", resolve: {
                model: "LogEntry"}}).
        when('/:appID/users', { controller: "ListCtrl",
            templateUrl: "/static/tmpl/logs.tmpl", resolve: {
                model: "User"}}).
        when('/:appID/devices', { controller: "ListCtrl",
            templateUrl: "/static/tmpl/logs.tmpl", resolve: {
                model: "Device"}}).
        when('/:appID/profiles', { controller: "ListCtrl",
            templateUrl: "/static/tmpl/profiles.tmpl", resolve: {
                model: "Profile"}}).
//       when('/', {controller:MainCtrl, templateUrl:'main.html'}).
// //      when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
// //      when('/new', {controller:CreateCtrl, templateUrl:'detail.html'}).
      otherwise({redirectTo:'/'});
  }).
  controller ("NavbarCtrl", function($scope, appState){
    $scope.appState = appState;

  }).
  controller ("ListCtrl", function($scope, appState, model, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.list = model.query({'_key': app.key});
  }).
  controller ("DashboardCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.name = app.name;
    $scope.key = app.key;
    $scope.secret = app.secret;
  }).
  controller ("DeviceDetailsCtrl", function($scope, appState, Device, LogEntry, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    var device = Device.get({deviceID: $routeParams.deviceID, '_key': app.key});
    $scope.id = $routeParams.deviceID;
    $scope.device = device;
    $scope.logs = LogEntry.query({'_key': app.key, "device": $routeParams.deviceID });
  }).
  controller ("AppDetailsCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.name = app.name;
    $scope.key = app.key;
    $scope.secret = app.secret;
  }).
  controller ("AddProfileCtrl", function ($scope, $location, Profile, appState) {
    $scope.name = null;

    $scope.saveProfile = function() {
      var app = appState.selected_app,
          newProfile = new Profile({"name": $scope.name, "appKey": app.key});
      if (!app.profiles) app.profiles = [];

      $scope.name = null;
      newProfile.$save(function() {

        // appState.addProfile(newProfile);
        app.profiles.push(newProfile);
        $scope.dismiss();
        $location.path("/" + appState.selected_app.key + "/profiles/" + newProfile.id);
      });
    };
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