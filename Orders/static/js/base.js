var OrdersApp = angular.module('OrdersApp', ['ngRoute', 'ui-notification', 'ngMask']);

OrdersApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
}).config(['$locationProvider', function($locationProvider) {
  $locationProvider.hashPrefix('');
}]).config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-CSRFToken'] = angular.element(document.querySelector("[name='csrfmiddlewaretoken']")).val();
}]).config(function(NotificationProvider) {
    NotificationProvider.setOptions({
        delay: 3000,
        startTop: 20,
        startRight: 10,
        verticalSpacing: 20,
        horizontalSpacing: 20,
        positionX: 'right',
        positionY: 'top',
    });
});
