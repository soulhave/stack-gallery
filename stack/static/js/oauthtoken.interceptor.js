
// auth interceptor to handle oauth token
app.factory('BearerAuthInterceptor', function ($rootScope, $q, $window) {
    return {
        request: function(config) {
            // console.log('request => method: ' + config.method + ' url: ' + config.url);

            config.headers = config.headers || {};
            token = window.localStorage.oauthToken
            if (token !== null && token !== 'null') {
            	// console.log('add header Authorization ' + token);
            	config.headers.Authorization = token
        	}

            return config || $q.when(config);
        },
        response: function(response) {
        	// console.log('response => status: ' + response.status + ' url: ' + response.config.url);
        	// console.log(response.headers('Authorization'));

        	window.localStorage.setItem('oauthToken', response.headers('Authorization'))
            if (response.status === 401) {
                //  Redirect user to login page / signup Page.
            }
            return response || $q.when(response);
        }
    };
});

// Register the previously created AuthInterceptor.
app.config(function ($httpProvider) {
    $httpProvider.interceptors.push('BearerAuthInterceptor');
});