
angular.module('console.services', ['ngResource', 'ui']).
  factory('App', function($resource){
    return $resource('/api/v1/my_apps/:appID', {appID: "@key"}, {
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
      link: function(scope, element, attr, ctrl) {
          var $el = $(element);
          $el.modal("hide");
          scope.show = function() {
            $el.modal("show");
          };
          scope.dismiss = function() {
            $el.modal("hide");
          };
          $el.on("show", function(){
            scope.$emit("modalShow", arguments);
          });
          $el.on("shown", function(){
            scope.$emit("modalShown", arguments);
          });
          $el.on("hide", function(){
            scope.$emit("modalHide", arguments);
          });
          $el.on("hidden", function(){
            scope.$emit("modalHidden", arguments);
          });
        }
      };
  }).
  directive('editable', function() {
    return {
      require: 'ngModel',
      link: function(scope, elm, attrs, model) {
        elm.editable($.extend({
          emptytext: "(empty)",
          "emptyclass": "",
          "unsavedclass": ""
        }, scope.$eval(attrs.editable)));
        model.$render = function() {
            elm.editable('setValue', model.$viewValue);
        };
        elm.on('save', function(e, params) {
            model.$setViewValue(params.newValue);
            scope.$apply();
        });
        if (attrs.editableSaved) {
          elm.on('save', function(){
            scope.$eval(attrs.editableSaved);
           });
        }
      }
    };
  }).
  service('appState', function(App, Profile, $rootScope){
    var self = this;
    self.selected_app = null;
    self.profiles = null;
    self.timeOptions = [
        {value: 1, name: "second"},
        {value: 60, name: "minute"},
        {value: 1800, name: "half an hour"},
        {value: 3600, name: "hour"},
        {value: 7200, name: "2 hours"},
        {value: 14400, name: "4 hours"},
        {value: 28800, name: "8 hours"},
        {value: 43200, name: "12 hours"},
        {value: 86400, name: "24 hours"},
        {value: 86401, name: "day"},
        {value: 172800, name: "2 days"},
        {value: 432000, name: "5 days"},
        {value: 604800, name: "7 days"},
        {value: 604801, name: "week"},
        {value: 1209600, name: "2 weeks"},
        {value: 2419200, name: "4 weeks"},
        {value: 30758401, name: "year"}
      ];

    self.selectApp = function(app) {
      if (!app.profiles) app.profiles = Profile.query({_key:app.key});
      self.selected_app = app;
      self.profiles = app.profiles;
    };

    self.addApp = function(app) {
      self.apps.push(app);
      self.selectApp(app);
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
      if (self.apps.length === 0){
        $rootScope.$broadcast("show-add-app");
        console.log("yes");
      } else {
        self.selectApp(self.apps[0]);
      }
    });

    $rootScope.appState = self;
  });

var consoleApp = angular.module('console', ["console.services"]).
  config(function($routeProvider) {
     $routeProvider.
        when('/:appID/details', { controller: "AppDetailsCtrl",
            templateUrl: "/static/tmpl/app_details.tmpl"}).
        when('/:appID/dashboard', { controller: "DashboardCtrl",
            templateUrl: "/static/tmpl/dashboard.tmpl"}).
        when('/:appID/stats', { controller: "StatsCtrl",
            templateUrl: "/static/tmpl/stats.tmpl"}).

        when('/:appID/devices/:deviceID', { controller: "DeviceDetailsCtrl",
            templateUrl: "/static/tmpl/device_details.tmpl"}).

        when('/:appID/profiles/:profileID', { controller: "ProfileDetailsCtrl",
            templateUrl: "/static/tmpl/profile_details.tmpl"}).

        when('/:appID/users/:userID', { controller: "UserDetailsCtrl",
            templateUrl: "/static/tmpl/user_details.tmpl"}).

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
//       when('/', {controller: "MainCtrl", templateUrl:'main.html'}).
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
  controller ("StatsCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.app = app;
  }).
  controller ("DashboardCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.app = app;
  }).
  controller ("ProfileDetailsCtrl", function($scope, appState, $rootScope, Profile, LogEntry, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    var profile = Profile.get({profileID: $routeParams.profileID, '_key': app.key});
    var timeNames = {};
    $.each(appState.timeOptions, function(idx, item) {
      timeNames[item.value] = item.name;
    });
    $scope.profile = profile;
    appState.profile = profile;
    $scope.saveModel = saveModel = function (){
      profile.$save({ '_key': app.key});
    };

    $scope.formatSettingsKey = function(keyName, value) {
      if (keyName === 'duration') {
        return timeNames[value] || moment.duration(value, "seconds").humanize();
      }
      return value;
    };
    $scope.editRestriction = function(idx) {
      $rootScope.$broadcast("editRestriction", {idx: idx,
          restriction: appState.profile.restrictions[idx]
      });
    };
    $scope.deleteRes = function(idx) {
      profile.restrictions.splice(idx, 1);
      saveModel();
    };
    $scope.switchRes = function(first_idx, second_idx) {
      var first = profile.restrictions[first_idx];
      profile.restrictions[first_idx] = profile.restrictions[second_idx];
      profile.restrictions[second_idx] = first;
      saveModel();
    };
  }).
  controller ("DeviceDetailsCtrl", function($scope, appState, Device, LogEntry, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.id = $routeParams.deviceID;
    $scope.profile_options = $.map(appState.profiles, function(item) {
      return {value: item.id, text: item.name};
    });
    $scope.device = Device.get({deviceID: $routeParams.deviceID, '_key': app.key});
    $scope.logs = LogEntry.query({'_key': app.key, "device": $routeParams.deviceID });
    $scope.save = function() {
      $scope.device.assigned_profile_id = $scope.device.assigned_profile.id;
      $scope.device.$save({ '_key': app.key});
    };
    $scope.addItem = function(key, value){
        $scope.device.account[key] = value;
        $scope.save();
    };
    $scope.delAccountItem = function(key) {
      delete $scope.device.account[key];
      $scope.save();
    };
  }).
  controller ("UserDetailsCtrl", function($scope, appState, User, LogEntry, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.id = $routeParams.userID;
    $scope.profile_options = $.map(appState.profiles, function(item) {
      return {value: item.id, text: item.name};
    });
    $scope.app = app;
    $scope.user = User.get({userID: $routeParams.userID, '_key': app.key});
    $scope.logs = LogEntry.query({'_key': app.key, "user": $routeParams.userID });
    $scope.save = function() {
      $scope.user.assigned_profile_id = $scope.user.assigned_profile.id;
      $scope.user.$save({ '_key': app.key});
    };
    $scope.addItem = function(key, value){
        $scope.user.account[key] = value;
        $scope.save();
    };
    $scope.delAccountItem = function(key) {
      delete $scope.user.account[key];
      $scope.save();
    };
  }).
  controller ("AppDetailsCtrl", function($scope, appState, $routeParams){
    var app = appState.findAndSelectApp($routeParams.appID);
    $scope.app = app;
    $scope.saveModel = function() {
      app.$save();
    };
  }).
  controller ("AddRestrictionCtrl", function ($scope, $location, appState) {
    $scope.params = {};
    $scope.timeOptions = appState.timeOptions;
    $scope.$on("editRestriction", function(key, val) {
      $scope.idx = val.idx + 1; // prevent == 0
      angular.copy(val.restriction, $scope.params);
      $scope.show();
    });
    $scope.$on("modalHidden", function(){
      $scope.params = {};
      $scope.idx = false;
    });

    function get_params(params){
      var taking = {
        'BinaryRestriction': ['allow'],
        'PerTimeRestriction': ['limit_to', 'duration'],
        'AccountAmountRestriction': ['account_item', 'quantity_change'],
        'TotalAmountRestriction' : ['total_max'],
        'LocalAmountRestriction' : ['local_max']
      },
      res = {
        "class_": params.class_,
        "action": params.action
      };
      angular.forEach(taking[params.class_], function(name) {
        res[name] = params[name];
      });
      return res;
    }

    $scope.saveRestriction = function() {
      if ($scope.idx) {
        appState.profile.restrictions[$scope.idx -1] = get_params($scope.params);
      } else {
        appState.profile.restrictions.push(get_params($scope.params));
      }
      $scope.params = {};
      appState.profile.$save({ '_key': appState.selected_app.key});
      $scope.dismiss();
    };
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
  run(function(appState, $rootScope) {
    var ju;
    jerry.init("agxkZXZ-ai1lcnJpY29yEAsSCUFwcEFjY2VzcxjpBww", "/api/v1/");
    jerry.customMethods["permission_state"] = "/api/v1/local_permission_state";
    appState.jerryUser = ju = jerry.signin();
    appState.userCan = {};
    function updateCan() {
      $rootScope.$apply(function() {
        appState.userCan = ju.getCans();
      });
    }
    ju.on("did", updateCan);
    ju.promise.then(updateCan);
  }).
  controller ("AddAppCtrl", function ($scope, $location, App, appState) {
    $scope.model = {};

    $scope.saveApp = function() {
      var newApp = new App({name: $scope.model.app_name,
            template:$scope.model.template});
      $scope.model.app_name = null;
      newApp.$save(function() {

        appState.addApp(newApp);
        $scope.dismiss();
        $location.path("/" +  newApp.key + "/details/");
      });
    };
    $scope.$on("show-add-app", function() {
      $scope.show();
    });
  });