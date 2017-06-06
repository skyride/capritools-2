var app = angular.module('myApp', []);
	app.controller('myCtrl', function($scope, $http, $location) {
	$scope.minerals = minerals;
	$scope.towers = towers;
	$scope.blocks = blocks;

	$scope.active = $scope.towers[0].id;
	$scope.sovbonus = false;

	$scope.isk = function(isk) {
		return numeral(isk).format('0,0.00') + " ISK";
	};


	$scope.getFuelCost = function() {
		var tower = $scope.getTower($scope.active);
		var block = $scope.getBlock(tower.blockid);
		var cost = block.sell * $scope.getUsage(tower.usage) * 24 * 30;
		return cost;
	};

	$scope.income = function(sell) {
		return sell * 100 * 30 * 24;
	}

	$scope.profitClass = function(isk) {
		if(isk >= 0) {
			return "text-success";
		} else {
			return "text-danger";
		}
	}

	$scope.getUsage = function(usage) {
		if($scope.sovbonus == true) {
			return Math.round(usage * 0.75);
		} else {
			return usage;
		}
	}


	$scope.activeTower = function() {
		return $scope.getTower($scope.active);
	}

	$scope.getMineral = function(id) {
		for(i = 0; i < $scope.minerals.length; i++) {
			if($scope.minerals[i].id == id) {
				return $scope.minerals[i];
			}
		}
	};

	$scope.getTower = function(id) {
		for(i = 0; i < $scope.towers.length; i++) {
			if($scope.towers[i].id == id) {
				return $scope.towers[i];
			}
		}
	};

	$scope.getBlock = function(id) {
		for(i = 0; i < $scope.blocks.length; i++) {
			if($scope.blocks[i].id == id) {
				return $scope.blocks[i];
			}
		}
	};
});
