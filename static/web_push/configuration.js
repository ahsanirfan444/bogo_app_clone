// Utils functions:

function urlBase64ToUint8Array(base64String) {
    var padding = '='.repeat((4 - base64String.length % 4) % 4)
    var base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/')

    var rawData = window.atob(base64)
    var outputArray = new Uint8Array(rawData.length)

    for (var i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i)
    }
    return outputArray;
}
function loadVersionBrowser(userAgent) {
    var ua = userAgent, tem, M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if (/trident/i.test(M[1])) {
        tem = /\brv[ :]+(\d+)/g.exec(ua) || [];
        return { name: 'IE', version: (tem[1] || '') };
    }
    if (M[1] === 'Chrome') {
        tem = ua.match(/\bOPR\/(\d+)/);
        if (tem != null) {
            return { name: 'Opera', version: tem[1] };
        }
    }
    M = M[2] ? [M[1], M[2]] : [navigator.appName, navigator.appVersion, '-?'];
    if ((tem = ua.match(/version\/(\d+)/i)) != null) {
        M.splice(1, 1, tem[1]);
    }
    return {
        name: M[0],
        version: M[1]
    };
};


function requestPOSTToServer(data) {
    fetch('/device/web/', { method: 'POST', body: JSON.stringify(data), headers: { 'Content-Type': 'application/json' } }).then(response => {
        console.log("success");
    })

}


var applicationServerKey = server_key;
// if (Notification.permission !== "granted") {
if(registered == false){
    // In your ready listener
    if ('serviceWorker' in navigator) {
        // The service worker has to store in the root of the app
        // http://stackoverflow.com/questions/29874068/navigator-serviceworker-is-never-ready
        var browser = loadVersionBrowser('chrome');
        navigator.serviceWorker.register('/static/web_push/navigatorPush.service.js').then(function (reg) {
            reg.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(applicationServerKey)
            }).then(function (sub) {
                var endpointParts = sub.endpoint.split('/');
                var registration_id = endpointParts[endpointParts.length - 1];
                if (browser.version.indexOf("Chrome") != -1) {
                    browser.name = "chrome";
                }
                var data = {
                    'browser': browser.name.toUpperCase(),
                    'p256dh': btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('p256dh')))),
                    'auth': btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('auth')))),
                    'name': navigator.userAgent.match(/^[^\(]+\((\w+)/).toString(),
                    'registration_id': registration_id,
                    'user': user_id
                };
                requestPOSTToServer(data)

            })
        }).catch(function (err) {
            console.log(':^(', err);
        });

    }
}

