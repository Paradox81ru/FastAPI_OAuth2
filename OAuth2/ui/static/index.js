document.addEventListener('DOMContentLoaded', function() {
    const host = window.location.origin;

    const formAuth = document.getElementById("formAuth");
    const fieldUsername = document.getElementById("fldUsername");
    const fieldPassword = document.getElementById("fldPassword");
    const checkboxScopeMe = document.getElementById("chbScopeMe");
    const checkboxScopeItems = document.getElementById("chbScopeItems");
    const btnRequestTokens = document.getElementById("btnRequestTokens");

    const fieldTokenAccess = document.getElementById("fldTokenAccess");
    const fieldTokenRefresh = document.getElementById("fldTokenRefresh");
    const btnTokenRefresh = document.getElementById("btnTokenRefresh");

    btnTokenRefresh.addEventListener("click", requestTokenHandler)

    function requestTokenHandler(ev) {
        authorization();
    }

    function authorization() {
        const api = "/api/oauth/token";
        const formData = new FormData(formAuth);

        apiRequest("POST", api, successfulReceiptOfTokens, errorReceiptOfTokens, data=formData);
    }

    /**
     * Функция обработки успешного получения токенов
     * @param {У} data 
     */
    function successfulReceiptOfTokens(data) {
        alert(data);
    }

    /**
     * Ошибка при получении токенов
     * @param {*} statusText 
     * @param {*} response 
     */
    function errorReceiptOfTokens(statusText, response) {
        alert(statusText + " " + response);
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
    function apiRequest(method, api, successCallback, failedStatusCallback, headers={}, data={}) {
        const url=`${host}${api}`;
        const requiredHeaders = {"content-type": "application/json; charset=UTF-8"};
        Object.assign(headers, requiredHeaders);


        let options = {
            headers: headers,
            method: method,
        };

        // Если переданы доанные формы,
        if (data instanceof FormData) {
            // то эту форму передает в тело запроса.
            options['body'] = data;
        } else if ((typeof (data) === 'object') && !(isObjectEmpty(data))) {
            // Иначе эти данные должны быть переданы в свойстве body в виде параметра.
            options['body'] = getSearchParams(args.data);
        }

        fetch(url, options)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new StatusError(response.statusText, response)
            }
        })
        .then(data => {
            successCallback(data);
        })
        .catch(error => {
            failedStatusCallback(error.message, error.respons)
        });
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

class StatusError extends Error {
    constructor(message, response) {
        super(message);
        this.name = "StatusError";
        this.response = response;
    }
}