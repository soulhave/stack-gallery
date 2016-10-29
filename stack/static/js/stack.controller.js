app.controller('AppCtrl', ['$scope', '$mdBottomSheet','$mdSidenav', '$mdDialog', '$resource', function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, $resource){
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  var StackApi = $resource('stack');
  StackApi.query(function(projects){
    $scope.projects = projects;         
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