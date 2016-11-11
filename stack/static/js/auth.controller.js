app.controller('AuthController', ['$scope', '$http', '$location', '$auth', '$mdToast', 
  function($scope, $http, $location, $auth, $mdToast){

  $scope.isAuthenticated = function() {
    console.log('isAuthenticated - ' + $auth.isAuthenticated())
    return $auth.isAuthenticated();
  };

  $scope.authenticate = function(provider) {
    console.log('authenticate' + provider)
    $auth.authenticate(provider, {accessType: 'offline'})
      .then(function() {
        $mdToast.show(
          $mdToast.simple()
            .textContent('You have successfully signed in with ' + provider + '!')
            .position('top right')
            .hideDelay(3000)
        );        
        // toastr.success('You have successfully signed in with ' + provider + '!');
        $location.path('/');
      })
      .catch(function(error) {
        if (error.message) {
          // Satellizer promise reject error.
          $mdToast.show(
            $mdToast.simple()
              .textContent(error.message)
              .position('top right')
              .hideDelay(5000)
          );                  
        } else if (error.data) {
          // HTTP response error from server
          // toastr.error(error.data.message, error.status);
          $mdToast.show(
            $mdToast.simple()
              .textContent(error.data.message + ' - ' + error.status)
              .position('top right')
              .hideDelay(5000).toastClass('error')
          );             
        } else {
          $mdToast.show(
            $mdToast.simple()
              .textContent(error)
              .position('top right')
              .hideDelay(5000)
          );   
        }
      });        
  };


  $scope.logout = function() {

    console.log('logout')

    if (!$auth.isAuthenticated()) { return; }
    $auth.logout()
      .then(function() {
          $mdToast.show(
            $mdToast.simple()
              .textContent('You have been logged out')
              .position('top right')
              .hideDelay(3000)
          );   

        // toastr.info('You have been logged out');
        // $location.path('/');
      });    

    $http.get('logout').success(function(lastData, status, headers) {  
                console.log('status logout ' + status)            
                if (status==302) {
                    //this doesn't work
                    //window.location=headers('Location');
                    //this doesn't work either
                    window.location.replace(headers('Location'));
                }else if (status==200) {
                    console.log('logout success. Redirecting')
                    window.location.href = "/"
                }
            });

    window.localStorage.clear();
  }

}]);