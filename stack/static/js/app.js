/**
* You must include the dependency on 'ngMaterial' 
*/

var app = angular.module('StarterApp', ['ngMaterial', 
  'ngMdIcons', 
  'ngResource', 
  'ngAnimate', 
  'angular-loading-bar', 
  'satellizer']);

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

app.config(function($authProvider) {

    console.log('provider google configured')
    $authProvider.google({
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

