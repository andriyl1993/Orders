OrdersApp.config(function($routeProvider) {
    $routeProvider
        // route for the auth home page
        .when('/', {
            controller  : 'AuthController',
        })
        .when('/login/', {
            templateUrl : '/static/js/templates/login.html',
            controller  : 'AuthController',
        })
        .when('/sign-up/', {
            templateUrl : '/static/js/templates/sign_up.html',
            controller  : 'AuthController',
        })
        .when('/logout/', {
            template : '<div ng-init="logout()"></div>',
            controller  : 'HeaderController',
        })
}).run( function($rootScope, $location) {
    $rootScope.$on("$routeChangeStart", function (event, next, current) {
        function change_hash(path) {
            if (path[path.length - 1] == '/')
                path = path.substring(0, path.length - 1);
            if (path[0] == '/' || path[0] == '#')
                path = path.substring(1, path.length);
            return path;
        }

        var current_path = $location.path();
        current_path = change_hash(current_path).split('/')[0];

        var header_elems = angular.element(document.getElementById('menu')).find('a');
        angular.element(header_elems).removeClass('active-link');
        angular.forEach(header_elems, function(val) {
            var path = change_hash(val.hash);
            if (path == current_path)
                angular.element(val).addClass('active-link');

        })
    });
});

OrdersApp.controller('HeaderController', function($scope, $http, Notification) {
    // name, link, auth (null - not check, false - not auth, true - auth)
    $scope.init_data = function(username) {
        $scope.is_auth = (username == '' ? false: true);
        $scope.menu = [
            ['Домашня', '/#', null],
            ['Заглушка', '#', null],
            ['Заглушка', '#', null],
            ['Заглушка', '#', null],
            ['Вийти', '#logout/', true],
            ['Авторизація', '#login/', false],
            ['Реєстрація', '#sign-up/', false],
            [username, '#', true],
        ];
    };

    $scope.logout = function() {
        $http.get('/user/logout/').then(
            function(res) {
                location.href= '/';
            },
            function (res) {
                var msg = 'Під час реєстрації сталася помилка'
                Notification.error({message: msg});
            }
        )
    };
});