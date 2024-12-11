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

    function authorization() {
        api = "/api/oauth/token";
        apiRequest("POST", api)
    }

    function apiRequest(method, api, headers={}, data=undefined) {
        const url=`${host}${api}`;
        const requiredHeaders = {"content-type": "application/json; charset=UTF-8"};
        Object.assign(headers, requiredHeaders);


        const otherParam = {
            headers: headers,
            method: method,
        };

        fetch(url, otherParam)
        .then(response => {
            if (!response.ok) {
                rStatus = response.status;
                let result = response.json();
                let errMsg = 'detail' in response ? response['detail'] : `Error staus ${rStatus}`;
                throw new Error(response.json()")
            } else {
                return response.json();
            }
        })
        .then(data => {
            return data;
        })
        .catch(error => userInfoField.value = error);
    }

});

