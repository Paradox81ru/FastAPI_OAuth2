document.addEventListener('DOMContentLoaded', function() {
    const host = window.location.origin;

    const formAuth = document.getElementById("formAuth");
    const alertDanger = document.getElementById("alertDanger");
    const fieldUsername = document.getElementById("fldUsername");
    const fieldPassword = document.getElementById("fldPassword");
    const checkboxScopeMe = document.getElementById("chbScopeMe");
    const checkboxScopeItems = document.getElementById("chbScopeItems");
    const btnRequestTokens = document.getElementById("btnRequestTokens");

    const fieldTokenAccess = document.getElementById("fldTokenAccess");
    const fieldTokenRefresh = document.getElementById("fldTokenRefresh");
    const btnTokenRefresh = document.getElementById("btnTokenRefresh");
    const HTML_CLASS_HIDDEN = "d-none";

    btnRequestTokens.addEventListener("click", requestTokenHandler);
    btnTokenRefresh.addEventListener('click', requestRefreshTokenHandler);

    /**
     * Обработчик кнопик запроса токенов
     * @param {*} ev 
     */
    function requestTokenHandler(ev) {
        authorizationRequest();
    }

    /**
     * Обработчик кнопки обновления токенов
     * @param {*} ev 
     */
    function requestRefreshTokenHandler(ev) {
        tokenRefreshRequest();
    }

    /**
     * Запрос полчения токенов
     */
    function authorizationRequest() {
        const api = "/api/oauth/token";
        const formData = new FormData(formAuth);

        apiRequest("POST", host, api, successfulResponse, errorResponse, {}, formData);
    }

    /**
     * Запросо обновления токенов
     */
    function tokenRefreshRequest() {
        const api = "/api/oauth/token-refresh";
        const tokenRefresh = `bearer ${fieldTokenRefresh.value}`;
        const headers = {Authorization: tokenRefresh};

        apiRequest("POST", host, api, successfulResponse, errorResponse, headers, {});
    }

    /**
     * Функция обработки успешного получения токенов
     * @param {У} data 
     */
    function successfulResponse(data) {
        hideAllertDanger();
        fillTokenFields(data['access_token'], data['refresh_token'])
    }
 

    /**
     * Ошибка при ответе от срвера
     * @param {*} statusText 
     * @param {*} response 
     */
    function errorResponse(statusText, statusCode, response) {
        clearTokenFields();
        if ([400, 401].indexOf(statusCode) != -1)
            response.then(responsen_json => {
                showAlertDanger(`Error: ${statusText} ${responsen_json['detail']}`);
        });
            // showAlertDanger(`Error: ${statusText} ${responsen['detail']}`);
        else {
            showAlertDanger(`Error: ${statusCode} - ${statusText}`);
        }
    }

    /**
     * Заполняет поля токенов данными
     * @param {String} accessToken 
     * @param {String} refreshToken 
     */
    function fillTokenFields(accessToken, refreshToken) {
        fieldTokenAccess.value = accessToken;
        fieldTokenRefresh.value =  refreshToken;
    }

    /**
     * Очищает поля токенов
     */
    function clearTokenFields() {
        fieldTokenAccess.value = '';
        fieldTokenRefresh.value = '';
    }


    /**
     * Отображет сообшение об ошибке
     * @param {String} msg сообшение об ошибке
     */
    function showAlertDanger(msg) {
        alertDanger.textContent = msg;
        if (alertDanger.classList.contains(HTML_CLASS_HIDDEN)) 
            alertDanger.classList.remove(HTML_CLASS_HIDDEN);
    }

    /**
     * Скрывает сообшение об ошибке
     */
    function hideAllertDanger() {
        if (!alertDanger.classList.contains(HTML_CLASS_HIDDEN)) {
            alertDanger.classList.add(HTML_CLASS_HIDDEN);
            alertDanger.textContent = "";
        }

    }
});

/**
 * Проверка на пустой объект
 * @param obj
 * @returns {boolean}
 */
function isObjectEmpty(obj) {
    for (let key in obj)
        if (obj.hasOwnProperty(key))
            return false;
    return true;
}

/**
 * Формирует и возвращает строку параметра запроса
 * @param data {Object}
 * @returns {string}
 */
function getSearchParams(data) {
    let searchParams = new URLSearchParams();
    for (let key in data)
        searchParams.append(key, data[key]);

    return searchParams.toString();
}

/**
 * API запрос
 * @param {String method} метод запроса
 * @param {String} api эндпоинт
 * @param {function} successCallback функция обратного вызова при успешном ответе
 * @param {function} failedStatusCallback функция обратного вызова при ошибке ответа
 * @param {{}} [headers={}] заголовки запроса
 * @param {{}} [data={}] данные запроса
 */
function apiRequest(method, host, api, successCallback, failedStatusCallback, headers={}, data={}) {
    const url=`${host}${api}`;
    const requiredHeaders = {"content-type": "application/json; charset=UTF-8"};
    Object.assign(headers, requiredHeaders);


    let options = {
        headers: headers,
        method: method,
    };

    // Если переданы доанные формы,
    if (data instanceof FormData) {
        delete (options.headers);
        // то эту форму передает в тело запроса.
        options['body'] = data;
    } else if ((typeof (data) === 'object') && !(isObjectEmpty(data))) {
        // Иначе эти данные должны быть переданы в свойстве body в виде параметра.
        options['body'] = getSearchParams(data);
    }

    fetch(url, options)
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
            // throw new ResonseError(response.statusText, response.status, response);
            throw new StatusError(response.statusText, response.status, response.json())
        }
    })
    .then(data => {
        successCallback(data);
    })
    .catch(error => {
        // return error.resopnse.json
       failedStatusCallback(error.message, error.statusCode, error.response)
    })
}

class StatusError extends Error {
    constructor(message, statusCode, response) {
        super(message);
        this.name = "StatusError";
        this.statusCode = statusCode;
        this.response = response;
    }
}

// class ResonseError extends Error {
//     constructor(message, statusCode, resopnse) {
//         super(message);
//         this.name = "StatusError";
//         this.statusCode = statusCode;
//         this.response = resopnse;
//     }
// }
