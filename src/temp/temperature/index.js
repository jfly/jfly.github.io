function TestCtrl($scope) {
    $scope.buttonClicks = 12;

    var socket = io.connect('http://localhost');
    socket.on('buttonClicks', function(data) {
        $scope.buttonClicks = data;
        $scope.$apply();
    });

    $scope.incrementCount = function() {
        $scope.buttonClicks += 1;
        socket.emit('buttonClicked', null);
    };
}
