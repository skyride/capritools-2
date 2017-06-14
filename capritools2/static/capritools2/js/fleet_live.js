angular.module('fleetLiveApp', [])
  .controller('fleetLiveController', function($scope, $http, $timeout) {
    var fleetLive = this;

    var loadTime = 5000;
    var loadPromise;
    fleetLive.fleet = {};

    var getData = function() {
      $http.get("/fleets/live/monolith/"+key).then(
        function(res) {
          fleetLive.fleet = res.data;
          nextLoad();
        }
      )
    };

    var cancelNextLoad = function() {
      $timeout.cancel(loadPromise);
    };

    var nextLoad = function(mill) {
      mill = mill || loadTime;

      cancelNextLoad();
      loadPromise = $timeout(getData, mill);
    }

    getData();

    $scope.$on('$destroy', function() {
      cancelNextLoad();
    });
  });
