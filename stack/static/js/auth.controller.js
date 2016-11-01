app.controller('AuthController', ['$scope', '$http', function($scope, $http){
  $scope.logout = function() {
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