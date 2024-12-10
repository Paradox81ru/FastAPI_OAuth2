document.addEventListener('DOMContentLoaded', function() {
    const tokenField = document.getElementById("token");
    const userInfoField = document.getElementById("user_info")
    const requestBtn = document.getElementById("btn_request")
    // Назначение обработчика кнопке щапроса информаци о пользователе
    requestBtn.addEventListener("click", requestBtnHandler)

    function getToken() {
        return tokenField.value
    }

    function requestBtnHandler() {
        /** Обработчик события для внопки запроса информации о пользователе */
        const host = window.location.origin;
        const api = "/api/get_user"
        const url=`${host}${api}`;
        const otherParam = {
            headers: {
                "content-type": "application/json; charset=UTF-8",
                "Authorization": `bearer ${getToken()}`
            },
            method: "GET",
        };

        fetch(url, otherParam)
            .then(data => data.json())
            .then(response => {
                userInfoField.value = convertResponse(response);
            })
            .catch(error => userInfoField.value = error);
    }

    function convertResponse(response) {
        /** Преобразует ответ */
        if ('detail' in response) {
            return `Error: ${response['detail']}`;
        } else {
            let result = "";
            for (key in response) {
                result += `${key}: ${response[key]}\n`;
            }
            return result;
        }
    }
});
