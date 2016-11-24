/**
* You must include the dependency on 'ngMaterial' 
*/

var app = angular.module('StarterApp', ['ngMaterial', 
  'ngMdIcons', 
  'ngResource', 
  'ngAnimate', 
  'angular-loading-bar',
  'ui.router', 
  'satellizer']);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);


app.run(function ($http) {
    $http.get('api/public/version').success(function (data) {
        console.log('init app')
        console.log(data)
    });
});

app.config(function($stateProvider, $urlRouterProvider, $authProvider) {

    /**
     * Helper auth functions
     */
    var skipIfLoggedIn = ['$q', '$auth', function($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.reject();
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }];

    var loginRequired = ['$q', '$location', '$auth', function($q, $location, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }];

    /**
     * App routes
     */
    $stateProvider
      .state('home', {
        url: '/',
        controller: 'HomeController',
        templateUrl: 'partials/home.html'
      })
      .state('login', {
        url: '/login',
        templateUrl: 'partials/login.html',
        controller: 'AuthController',
        resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
      })
      .state('logout', {
        url: '/logout',
        template: null,
        controller: 'AuthController'
      })
      .state('profile', {
        url: '/profile',
        templateUrl: 'partials/profile.html',
        controller: 'ProfileController',
        resolve: {
          loginRequired: loginRequired
        }
      })
      .state('stacks', {
        url: '/stacks',
        templateUrl: 'partials/stacks.html',
        controller: 'StackController',
        resolve: {
          loginRequired: loginRequired
        }
      });
    $urlRouterProvider.otherwise('/');

    console.log('provider google configured offline')
    $authProvider.google({
      optionalUrlParams: ['access_type', 'approval_prompt'],
      accessType: 'offline',
      approvalPrompt: 'auto',
      clientId: '146680675139-6fjea6lbua391tfv4hq36hl7kqo7cr96.apps.googleusercontent.com'
    });

});

// config theme colors

app.config(function($mdThemingProvider) {
  var customBlueMap =     $mdThemingProvider.extendPalette('light-blue', {
  'contrastDefaultColor': 'light',
  'contrastDarkColors': ['50'],
  '50': 'ffffff'
});

$mdThemingProvider.definePalette('customBlue', customBlueMap);

$mdThemingProvider.theme('default').primaryPalette('customBlue', {
  'default': '500',
  'hue-1': '50'
}).accentPalette('pink');

$mdThemingProvider.theme('input', 'default')
    .primaryPalette('grey')
});

