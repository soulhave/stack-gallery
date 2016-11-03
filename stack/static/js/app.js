/**
* You must include the dependency on 'ngMaterial' 
*/

var app = angular.module('StarterApp', ['ngMaterial', 'ngMdIcons', 'ngResource', 'ngAnimate', 'angular-loading-bar']);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);


app.run(function ($http) {
    $http.get('api/version').success(function (data) {
        console.log('init app')
        console.log(data)
    });
});

// auth interceptor to handle oauth token
app.factory('BearerAuthInterceptor', function ($rootScope, $q, $window) {
    return {
        request: function(config) {
            // console.log('request => method: ' + config.method + ' url: ' + config.url);

            config.headers = config.headers || {};
            token = window.localStorage.oauthToken
            if (token !== null && token !== 'null') {
            	// console.log('add header Authorization ' + token);
            	config.headers.Authorization = token
        	}

            return config || $q.when(config);
        },
        response: function(response) {
        	// console.log('response => status: ' + response.status + ' url: ' + response.config.url);
        	// console.log(response.headers('Authorization'));

        	window.localStorage.setItem('oauthToken', response.headers('Authorization'))
            if (response.status === 401) {
                //  Redirect user to login page / signup Page.
            }
            return response || $q.when(response);
        }
    };
});

// Register the previously created AuthInterceptor.
app.config(function ($httpProvider) {
    $httpProvider.interceptors.push('BearerAuthInterceptor');
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

