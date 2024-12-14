document.addEventListener('DOMContentLoaded', function() {
    const HTML_CLASS_HIDDEN = "d-none";
    const host = window.location.origin;

    const tokenField = document.getElementById("token");
    const userInfoField = document.getElementById("user_info");
    const requestBtn = document.getElementById("btn_request");
    // Назначение обработчика кнопке щапроса информаци о пользователе
    requestBtn.addEventListener("click", getUserRequest);

    /**
     * Запрашивает пользователя по указанному токену
     */
    function getUserRequest() {
        const api = "/api/get_user";
        const tokenRefresh = `bearer ${tokenField.value}`;
        const headers = {Authorization: tokenRefresh};

        apiRequest("GET", host, api, successfulResponse, errorResponse, headers, {});
    }

    /**
     * Функция обработки успешного получения токенов
     * @param {*} data 
     */
        function successfulResponse(data) {
            hideAllertDanger();
            fillUserFields(data);
        }
     
    
        /**
         * Ошибка при ответе от срвера
         * @param {*} statusText 
         * @param {*} response 
         */
        function errorResponse(statusText, statusCode, response) {
            clearUserFields();
            if ([400, 401].indexOf(statusCode) != -1)
                response.then(responsen_json => {
                    showAlertDanger(`Error: ${statusText}. ${responsen_json['detail']}`);
            });
            else {
                showAlertDanger(`Error: ${statusCode} - ${statusText}`);
            }
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

    /**
     * Заполняет поле пользователя
     * @param {*} response ответ от сервера
     */
    function fillUserFields(response){
        userInfoField.value = convertResponseToUser(response);
    }

    /**
     * Преобразует ответ в данные о пользователе
     * @param {*} response 
     * @returns 
     */
        function convertResponseToUser(response) {
            user = response[0];
            scopes = response[1]
            let result = "";
            for (prop in user) {
                result += `${prop}: ${user[prop]}\n`;
            }
            if (scopes.length > 0)
                result += `scopes: ${scopes.join(", ")}\n`;
            return result;
        }

    /**
    * Очищает поле пользователя
    */
    function clearUserFields() {
        userInfoField.value = "";
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