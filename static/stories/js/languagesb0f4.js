const lng = {

    txt : {},

    init : function (lang) {
        this.txt = this._getMessagesByLang(lang);
    },

    _getMessagesByLang: function(lng) {
        return this._messages[lng?lng:'en'];
    },

    get: function(key) {
        return this.txt[key] ? this.txt[key] : key;
    },

    _messages : {
        'en' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'ru' : {
            'user_not_found'  : "Пользователь не найден, попробуйте еще раз.",
            'user_removed'  : "Пользователь удален по просьбе.",
            'user_private'  : "Данный аккаунт приватний.",
        },
        'de' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'fr' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'it' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'es' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'pt' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'tr' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'hi' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'ko' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
        'id' : {
            'user_not_found'  : "User not found, please try again.",
            'user_removed'  : "User removed on request.",
            'user_private'  : "This account is private.",
        },
    }
}
