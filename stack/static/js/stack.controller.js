app.controller('StackController', ['$scope', '$mdDialog', '$resource', '$timeout', '$mdSidenav', '$log', function($scope, $mdDialog, $resource, $timeout, $mdSidenav, $log){

  $scope.input = ''

  var StackAPI = $resource('api/stacks/:action', 
      { q : '@q' }, 
      {
        list : { method : 'GET', isArray: true },
        search : { method : 'GET', params : {action : 'search'}, isArray: true }
      }
  );  

  $scope.search = function() {
    q = $scope.input
    if (q == '' || q == null) {
      q = "*"
    }

    StackAPI.search({ q: q }, function(data){
      $scope.projects = data;
    });
  };

  //var StackApi = $resource('stack');
  StackAPI.list(function(data){
    console.log('list all')
    $scope.projects = data;         
  });

  // ----------------------------
  // -- Team view. Modal per stack id
  // ----------------------------
  $scope.showTeam = function(ev, id) {
    console.log('show team')
    // GET team for stack id
    url = 'api/stacks/team/' + id
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

  // ----------------------------
  // -- Key press feature ng-keyup function
  // ----------------------------
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

  // ----------------------------
  // -- Left NavBard
  // ----------------------------
  var TrendsAPI = $resource('api/trends/:action', 
      { q : '@q' }, 
      {
        owners : { method : 'GET', params : {action : 'owners'}, isArray: true },
        techs : { method : 'GET', params : {action : 'technologies'}, isArray: true }
      }
  );  

  TrendsAPI.owners(function(data){
    console.log('list owners') 
    $scope.owners = data;         
  });    

  TrendsAPI.techs(function(data){
    $scope.techs = data;         
  });  

  $scope.toggleLeft = function () {
    $mdSidenav('left').toggle()
      .then(function () {
        $log.debug("close LEFT is done");
      });
  }

  $scope.close = function () {
    $mdSidenav('left').close()
      .then(function () {
        $log.debug("close LEFT is done");
      });
  };  

  $scope.toggleLeft();

  $scope.ownersSelected = [];
  $scope.techsSelected = [];
  /*
   * Function called when checkbox is selected to filter
   * stack cards. List ownersSelected and techsSelected 
   * will be used
   */
  $scope.toggle = function (item, list) {
    $log.debug('toggle')
    var idx = list.indexOf(item);
    if (idx > -1) {
      list.splice(idx, 1);
    }
    else {
      list.push(item);
    }

    // -- trigger search by owners and techs
    // $log.debug(buildQueryParam('owner', list))
    queryOwners = buildQueryParam('owner', $scope.ownersSelected)
    queryTechs = buildQueryParam('stack.technologyName', $scope.techsSelected)
    param =  queryOwners + ' AND ' + queryTechs
    $log.debug('query parma: ' + param)
    $log.debug("changeItem - searching");

    StackAPI.search({ q: param }, function(data){
      $scope.projects = data;
    });    

  };

  function buildQueryParam(field, list) {
    if (list.length > 0) {    
      var query = field + ':(';
      var first = list[0];
      query = query + first.name;
      for (var i = 1; i < list.length; i++) {
        item = list[i];
        query = query + ' OR ' + item.name;
      }
      query = query + ')';
      return query;
    } else {
      return '*';
    }
  }


  // ----------------------------
  // -- Favorite Actions
  // ----------------------------
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