app.controller('LeftController', ['$scope', '$mdSidenav', '$resource', '$log', function($scope, $mdSidenav, $resource, $log){

  $scope.checkbox

  buildToggler('left');

  $scope.toggleLeft = buildToggler('left');

  function buildToggler(componentId) {
    return function() {
      $mdSidenav(componentId).toggle();
    }
  }

  $scope.close = function () {
    // Component lookup should always be available since we are not using `ng-if`
    $mdSidenav('left').close()
      .then(function () {
        $log.debug("close LEFT is done");
      });
  };

  var TrendsAPI = $resource('api/trends/:action', 
      { q : '@q' }, 
      {
        owners : { method : 'GET', params : {action : 'owners'}, isArray: true },
        techs : { method : 'GET', params : {action : 'technologies'}, isArray: true }
      }
  );  

  TrendsAPI.owners(function(data){
    console.log(data)
    $scope.owners = data;         
  });    

  TrendsAPI.techs(function(data){
    $scope.techs = data;         
  });

}]);
