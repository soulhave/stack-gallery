app.controller('AppCtrl', ['$scope', '$mdBottomSheet','$mdSidenav', '$mdDialog', '$resource', function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, $resource){

  $scope.input = ''

  $scope.search = function() {

    q = $scope.input
    if (q == '' || q == null) {
      q = "*"
    }

    Stack.search({ q: q }, function(data){
      $scope.projects = data;
    });
};

  var Stack = $resource('api/stack/:action', 
      { q : '@q' }, 
      {
        list : { method : 'GET', isArray: true },
        search : { method : 'GET', params : {action : 'search'}, isArray: true }
      }
  );

  //var StackApi = $resource('stack');
  Stack.list(function(data){
    $scope.projects = data;         
  });

  $scope.showTeam = function(ev, stack_id) {

    // GET team for stack id
    url = 'stack/team/' + stack_id
    var TeamApi = $resource(url);
    TeamApi.query(function(data){
      $mdDialog.show({
        controller: DialogController,
        templateUrl: 'dialog-team',
        targetEvent: ev,
        locals : {team : data},
        clickOutsideToClose: true,
        escapeToClose: true
      })
      .then(function(answer) {
        $scope.alert = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.alert = 'You cancelled the dialog.';
      });
    });  
  };

  $scope.likeCount = 2

  $scope.like = function(item) {
    item.like_count += 1
    console.log('TODO: async call to update like action' + item.key)
  }  

  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };  

}]);

function DialogController($scope, $mdDialog, team) {
  $scope.team =  team

  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
};