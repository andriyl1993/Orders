OrdersApp.config(function($routeProvider) {
    $routeProvider
    .when('/login/forgot/', {
        controller  : 'AuthController',
        templateUrl : '/static/js/templates/forgot.html'
    })
    .when('/login/restore/', {
        controller  : 'AuthController',
        templateUrl : '/static/js/templates/login_restore.html'
    })
});

OrdersApp.controller('AuthController', function($scope, $http, Notification) {
    $scope.login = function() {
        var login_data = this.login_data;
        login_data['remember'] = this.LoginForm.remember.$viewValue;
        $http.post('/user/login/', {'data-MyUser': login_data}).then(
            function(res) {
                location.href = '/';
            }, function(res) {
                if (res['data']['error'] == 'invalid_login')
                    var msg = 'Введені не коретні дані';
                else if (res['data']['error'] == 'invalid_form')
                    var msg = 'Дані не віповідають мінімальним вимогам';
                else
                    var msg = 'Під час авторизації сталася помилка'
                Notification.error({message: msg});
            }
        )
    };

    $scope.signup = function() {
        var signup_data = this.signup_data;
        $http.post('/user/sign-up/', {'data-MyUser': signup_data}).then(
            function(res) {
                Notification.success('Реєстрація пройшла успішно').then(function(res) {
                    res.onClose = function() {
                        location.hash = "#/login/";
                        Notification.info({message: 'Вам на почту надіслано листа для підтвердження реєстрації'})
                    }
                });
            }, function(res) {
                if (res['data']['error'] == 'invalid_signup')
                    var msg = 'Даний користувач вже зареєстрований';
                else if (res['data']['error'] == 'invalid_form')
                    var msg = 'Дані не віповідають мінімальним вимогам';
                else
                    var msg = 'Під час реєстрації сталася помилка'
                Notification.error({message: msg});
            }
        )
    };

    $scope.forgot_password_send = function () {
        var forgot_data = this.forgot_data;
        $http.post('/user/forgot/', {'data-MyUser': forgot_data}).then(
            function() {
                Notification.success('Повідомлення надіслане на вказану електронну адресу').then(function(res) {
                    res.onClose = function() {
                        location.hash = "#/login/restore/";
                        Notification.info({message: 'Введіть число з надісланого листа і введіть новий пароль'})
                    }
                });
            },
            function(res) {
                Notification.error({message: res['data']['error']});
            }
        )
    };

    $scope.restore_password_send = function () {
        var forgot_data = this.login_restore;
        $http.post('/user/restore/', {'data-RestorePassword': forgot_data}).then(
            function() {
                Notification.success('Повідомлення надіслане на вказану електронну адресу').then(function(res) {
                    res.onClose = function() {
                        location.hash = "#/login/restore/";
                        Notification.info({message: 'Введіть число з надісланого листа і введіть новий пароль'})
                    }
                });
            },
            function(res) {
                Notification.error({message: res['data']['error']});
            }
        )
    }
});