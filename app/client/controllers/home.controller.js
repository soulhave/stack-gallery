app.controller('HomeController', ['$scope', '$http', '$auth', function($scope, $http, $auth) {
    
    // TODO - use Account resources
    if ($auth.isAuthenticated()) {
        $http.get('/api/users/me')
        .then(function(response) {
                return response.data;
            }).catch(function(e) {
                console.log('Error: ', e);
                throw e;
            }).finally(function() {
                console.log('This finally block');
            });
    }

    // TODO - use 
    $http.jsonp('https://api.github.com/repos/marcuslacerda/stack-gallery?callback=JSON_CALLBACK')
      .success(function(data) {
        if (data) {
          if (data.data.stargazers_count) {
            $scope.stars = data.data.stargazers_count;
          }
          if (data.data.forks) {
            $scope.forks = data.data.forks;
          }
          if (data.data.open_issues) {
            $scope.issues = data.data.open_issues;
          }
        }
      });
  }]);
