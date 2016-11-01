app.controller('StackController', ['$scope', '$mdDialog', '$resource', '$timeout', function($scope, $mdDialog, $resource, $timeout){

  $scope.input = ''


  var StackAPI = $resource('api/stacks/:action', 
      { q : '@q' }, 
      {
        list : { method : 'GET', isArray: true },
        search : { method : 'GET', params : {action : 'search'}, isArray: true }
      }
  );  

  $scope.searchAll = function() {
    $scope.input = ''
    StackAPI.list(function(data){
      $scope.projects = data;         
    });    
  }

  $scope.search = function() {

    q = $scope.input
    if (q == '' || q == null) {
      q = "*"
    }

    StackAPI.search({ q: q }, function(data){
      $scope.projects = data;
    });
  };

  $scope.keyPress = function(event){
    console.log(event.keyCode + ' - ' + event.altKey);
    // if keyCode = ENTER (#13) 
    if (event.altKey && event.keyCode == 70) {
      $scope.showSearch = true
      $timeout(function () { 
              document.getElementById('search_input').focus();
      }, 10);      
    }

    if ($scope.showSearch) { 
      if (event.keyCode == 13) {
        $scope.search()
      }
      // if keyCode = ESC (#27)
      if (event.keyCode == 27) {
        $scope.showSearch = false
      }
    }
  };

  //var StackApi = $resource('stack');
  StackAPI.list(function(data){
    $scope.projects = data;         
  });

  $scope.showTeam = function(ev, stack_id) {

    // GET team for stack id
    url = 'api/stacks/team/' + stack_id
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