function TemperatureCtrl($scope) {
    $scope.temperature = new Temperature();
}

function Temperature() {
    this.min = 0;
    this.max = 1000;

    this.metrics = [ 
        {
            name: 'Fahrenheit',
            symbol: '\u00B0F',
            freezing: 32,
            boiling: 212
        },
        {
            name: 'Celsius',
            symbol: '\u00B0C',
            freezing: 0,
            boiling: 100
        },
        {
            name: 'kelvin',
            symbol: 'K',
            freezing: 273.15,
            boiling: 373.15
        }
    ];

    this.currentMetric_ = this.metrics[0];
    this.value_ = 0;

    this.valueFromMetricToMetric = function(value, fromMetric, toMetric) {
        var scale = ( 1.0 * (toMetric.boiling - toMetric.freezing) /
                (fromMetric.boiling - fromMetric.freezing) );
        return scale*(value - fromMetric.freezing) + toMetric.freezing
    };

    function createGetter(metric) {
        return function() {
            return this.valueFromMetricToMetric(
                    this.value_, this.currentMetric_, metric);
        };
    }
    function createSetter(metric) {
        return function(value) {
            this.currentMetric_ = metric;
            this.value_ = this.valueFromMetricToMetric(
                    value, metric, this.currentMetric_);
        };
    }

    this.overflow = function(metric) {
        var value = this[metric.name];
        return value > this.max;
    };

    this.underflow = function(metric) {
        var value = this[metric.name];
        return value < this.min;
    };

    for(var i = 0; i < this.metrics.length; i++) {
        var metric = this.metrics[i];
        this.__defineGetter__(metric.name, createGetter(metric));
        this.__defineSetter__(metric.name, createSetter(metric));
    }
}

angular.module('ng').directive('toFixed', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attr, ngModel) {
            function toUser(value) {
                return parseFloat(value).toFixed(attr.toFixed);
            }
            // Note that we place this formatter at the front of the
            // $formatters array. One of the existing formatters requires that
            // the value is a number. This formatter returns a string.
            ngModel.$formatters.unshift(toUser);
        }
    };
});
