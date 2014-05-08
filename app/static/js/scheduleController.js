function WorkInterval(interval) {
    this.interval = interval;
    this.nzok = false;
    this.note = '';
}

app.controller('scheduleController', ['$scope', '$http', function ($scope, $http) {
    $scope.months = [];
    $scope.workIntervals = [ new WorkInterval([8, 18]) ];
    var __self = this;

    $scope.getSchedule = function (doctor) {
        $http({
            method: 'GET',
            url: '/shedule/calendar',
            params: {
                days: 60,
                doctor: doctor
            }
        }).success(function (data) {
            $scope.months = [];
            for (var i = 0; i < data.length; i++) {
                $scope.months.push(data[i]);
            }
        })
    }

    $scope.onDateClick = function (day) {
        if (day.date) {

            if (day.on_work) {
                if (!day.selected) {
                    _.each(__self.getDays(), function(d) { d.selected = false; });
                }
            } else {
                _.each(__self.getDays(), function (d) {
                    if (d.on_work)
                        d.selected = false
                });
            }

            day.selected = !day.selected;
        }
    }

    this.getDays = function () {
        var days = [];
        for (var i = 0; i < $scope.months.length; i++) {
            for (var j = 0; j < $scope.months[i].weeks.length; j++) {
                for (var k = 0; k < $scope.months[i].weeks[j].length; k++) {
                    days.push($scope.months[i].weeks[j][k]);
                }
            }
        }
        return days;
    }

    $scope.hasSelected = function () {
        return _.any(__self.getDays(), function (x) {
            return x.selected;
        })
    }

    $scope.setWorkHours = function (doctor) {
        for (var i = 0; i < $scope.workIntervals.length; i++) {
            if (__self.hasOverlappingInterval(i)) {
                alert("Има припокриващи се интервали!");
                return;
            }
        }
        var selectedDays = _.map(_.filter(__self.getDays(), function (x) {
            return x.selected;
        }), function (x) {
            return x.date;
        });
        $http({
            method: 'POST',
            url: '/shedule/calendar/add',
            data: {
                'days': selectedDays,
                'intervals': $scope.workIntervals,
                'doctor': doctor
            }
        }).success(function (data) {
            window.location = window.location;
        })
    }

    $scope.addWorkHours = function () {
        var lastInterval = $scope.workIntervals[$scope.workIntervals.length - 1].interval;
        var from = 8, to = 18;
        if (lastInterval[1] < 23) {
            from = lastInterval[1] + 0.5;
            to = lastInterval[1] + 1;
        }

        $scope.workIntervals.push(new WorkInterval([from, to]));
    }

    $scope.fromHour = function (interval_index) {
        var part = ($scope.workIntervals[interval_index].interval[0] % 1) * 60;
        if (part < 10)
            part = '0' + part;
        return Math.floor($scope.workIntervals[interval_index].interval[0]) + ":" + part;
    }

    $scope.toHour = function (interval_index) {
        var part = ($scope.workIntervals[interval_index].interval[1] % 1) * 60;
        if (part < 10)
            part = '0' + part;
        return Math.floor($scope.workIntervals[interval_index].interval[1]) + ":" + part;
    }

    this.hasOverlappingInterval = function(interval_index) {
        for (var i = 0; i < $scope.workIntervals.length; i++) {
            if (interval_index == i)
                continue;
            var interval1 = $scope.workIntervals[interval_index].interval;
            var interval2 = $scope.workIntervals[i].interval;
            if (interval2[0] < interval1[1] && interval2[1] > interval1[0]) {  //i2.from < i1.to and i2.to > i1.from
                return true;
            }
        }
    }

    $scope.is_overlapps = function (interval_index) {
        return __self.hasOverlappingInterval(interval_index);
    }
}]);

app.filter('dayFormat', function () {
    return function (date) {
        if (!date) return '';
        return new Date(date).getDate();
    }
});