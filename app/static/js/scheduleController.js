function WorkInterval(interval, nzok) {
    this.interval = interval;
    if (nzok)
        this.nzok = nzok;
    else
        this.nzok = false;
}

app.service('checkSchedule', ['$http', function ($http) {
    this.check = function () {
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
        });
    }
}]);

app.controller('scheduleController', ['$scope', '$http', 'checkSchedule', 'customFormatter', function ($scope, $http, checkSchedule, customFormatter) {
    $scope.months = [];
    $scope.workIntervals = [];
    $scope.note = '';
    var __self = this;

    $scope.init = function (doctor) {
        __self.doctor = doctor;
        __self.getSchedule();
    }

    __self.getSchedule = function () {
        $http({
            method: 'GET',
            url: '/shedule/calendar',
            params: {
                days: 60,
                doctor: __self.doctor
            }
        }).success(function (data) {
            $scope.months = [];
            for (var i = 0; i < data.length; i++) {
                $scope.months.push(data[i]);
            }
        });
    }

    $scope.onDateClick = function (day) {
        if (day.date) {

            if (day.on_work) {
                if (!day.selected) {
                    _.each(__self.getDays(), function (d) {
                        d.selected = false;
                    });
                }
            } else {
                _.each(__self.getDays(), function (d) {
                    if (d.on_work)
                        d.selected = false;
                });
            }

            day.selected = !day.selected;

            if (day.selected) {
                $scope.workIntervals = [];
                $scope.note = '';
                if (day.on_work) {
                    __self.load_day_schedules(day.date);
                }
            }
        }
    }

    __self.getDays = function () {
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
            url: '/shedule/calendar/set',
            data: {
                'days': selectedDays,
                'intervals': $scope.workIntervals,
                'note': $scope.note,
                'doctor': doctor
            }
        }).success(function (data) {
            window.location = window.location;
        })
    }

    $scope.addWorkHours = function () {
        var from = 8, to = 18;
        if ($scope.workIntervals.length > 0) {
            var lastInterval = $scope.workIntervals[$scope.workIntervals.length - 1].interval;
            if (lastInterval[1] < 23) {
                from = lastInterval[1] + 0.5;
                to = lastInterval[1] + 1;
            }
        }

        $scope.workIntervals.push(new WorkInterval([from, to]));
    }

    $scope.removeHour = function (interval_index) {
        $scope.workIntervals.splice(interval_index, 1);
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

    __self.hasOverlappingInterval = function (interval_index) {
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

    __self.load_day_schedules = function (date) {
        $http({
            method: 'GET',
            url: '/shedule/calendar/get_date/' + date + '/' + __self.doctor
        }).success(function (data) {
            if (!data)
                return;
            $scope.note = data.note;
            $scope.workIntervals = [];
            for (var i = 0; i < data.hours.length; i++) {
                var val = data.hours[i];
                $scope.workIntervals.push(new WorkInterval([val.from, val.to], val.nzok))
            }
        });
    }
}]);

app.filter('dayFormat', function () {
    return function (date) {
        if (!date) return '';
        return new Date(date).getDate();
    }
});