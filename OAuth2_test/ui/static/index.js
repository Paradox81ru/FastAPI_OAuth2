document.addEventListener('DOMContentLoaded', function() {
    const host = window.location.origin;

    const tokenField = document.getElementById("token");
    const userInfoField = document.getElementById("user_info");
    const requestBtn = document.getElementById("btn_request");
    // Назначение обработчика кнопке щапроса информаци о пользователе
    requestBtn.addEventListener("click", getUserRequest);

    // function getToken() {
    //     return tokenField.value
    // }

    // function requestBtnHandler() {
    //     /** Обработчик события для внопки запроса информации о пользователе */
    //     const host = window.location.origin;
    //     const api = "/api/get_user"
    //     const url=`${host}${api}`;
    //     const otherParam = {
    //         headers: {
    //             "content-type": "application/json; charset=UTF-8",
    //             "Authorization": `bearer ${getToken()}`
    //         },
    //         method: "GET",
    //     };

    //     fetch(url, otherParam)
    //         .then(data => data.json())
    //         .then(response => {
    //             userInfoField.value = convertResponse(response);
    //         })
    //         .catch(error => userInfoField.value = error);
    // }

    /**
     * Запрашивает пользователя по указанному токену
     */
    function getUserRequest() {
        const api = "/api/get_user"
        const tokenRefresh = `bearer ${tokenField.value}`;
        const headers = {Authorization: tokenRefresh};

        apiRequest("GET", host, api, successfulResponse, errorResponse, headers, {});
    }

    /**
     * Функция обработки успешного получения токенов
     * @param {У} data 
     */
        function successfulResponse(data) {
            hideAllertDanger();
            userInfoField.value = convertResponse(response);
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
     * Преобразует ответ
     * @param {*} response 
     * @returns 
     */
    function convertResponse(response) {
        let result = "";
        for (key in response) {
            result += `${key}: ${response[key]}\n`;
        }
        return result;
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