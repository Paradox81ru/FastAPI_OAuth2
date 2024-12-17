/**
 * Класс проверки прав
 */
class RightsVerification {
    /**
     * 
     * @param {HTMLElement} block блок в котором должны быть созданы кнопки
     */
    constructor(block) {
        this.block = block
        this.api_list = ["scope/me", "scope/me_items", "only_admin", "only_director", "only_admin_or_director", "only_user", "only_authorized_user", "only_anonym_user"];
        // Объект списка всех значков с ключём API.
        this.badgeList = {};
    }

    init() {
        this.addButtonRows();
        this.addEventListner();
    }

    /**
     * Добавляет строки с кнопками
     */
    addButtonRows() {
        for (let api of this.api_list)
            this.block.appendChild(this.createRow(api));
    }

    /**
     * Добавляет обработчик для нажатия на кнопки
     */
    addEventListner() {
        this.block.addEventListener('click', (ev) => this.buttonClickHandler(ev));
    }

    /**
     * Обработчик нажатия кнопок
     * @param {MouseEvent} event 
     */
    buttonClickHandler(event) {
        /** @param {HTMLButtonElement} */
        let button = event.target;
        if (button.nodeName != 'BUTTON')
            return;

        const api = button.getAttribute('data-api');
        alert(api);
        this.setBadge(api, 'ok');
    }

    /**
     * Устанавливает badge
     * @param {String} api 
     * @param {String} Параметр установки ok, invalid или hide.
     */
    setBadge(api, param) {
        switch(param) {
            case 'ok':
                this.setBadgeOk(api);
                break;
            case 'invalid':
                this.setBadgeInvalid(api);
                break;
            case 'hide':
                this.setBadgeHide(api);
                break;
        }
    }

    /**
     * Устанавливает значёк в Ok
     * @param {String} api 
     */
    setBadgeOk(api) {
        /** @param {HTMLElement} */
        let badge = this.badgeList[api];
        if (badge.classList.contains('d-none'))
            badge.classList.remove('d-none');
        
        if (badge.classList.contains('text-bg-danger')) {
            badge.classList.remove('text-bg-danger');
            badge.classList.add('text-bg-success');
            badge.innerText = "Ok";
        }
    }

    /**
     * Устанавливает значёк в Invalid
     * @param {String} api 
     */
    setBadgeInvalid(api) {
        /** @param {HTMLElement} */
        let badge = this.badgeList[api];
        if (badge.classList.contains('d-none'))
            badge.classList.remove('d-none');

        if (badge.classList.contains('text-bg-success')) {
            badge.classList.remove('text-bg-success');
            badge.classList.add('text-bg-danger');
            badge.innerText = "Invalid";
        }
    }

    /**
     * Скрывает значёк
     * @param {String} api 
     */
    setBadgeHide(api) {
        let badge = this.badgeList[api];
        badge.classList.add('d-none')
    }

    /**
     * Создаёт строку проверки права
     * @param {String} api API по которой будет проверятся право
     * @returns 
     */
    createRow(api) {
        let div = this.createHTMLElement('div', ['mb-3', 'row'])
        div.appendChild(this.createButton(api));
        let badge = this.createSpanBadge();
        div.appendChild(badge);
        // Для дальнейшего урпавления значками, они все сохраняются в объект с ключём API.
        this.badgeList[api] = badge;        
        return div
    }

    /**
     * Создёет кнопку
     * @param {String} btnName Текст кнопки
     * @param {String} api API к которой относиться кнопка
     * @returns {HTMLElement}
     */
    createButton(api) {
        let classList = ['col-3', 'btn', 'btn-secondary'];
        let attrs = {type: 'button', 'data-api': api};
        return this.createHTMLElement('button', classList, attrs, api.replace(/[\/_]/g, ' '));
    }

    /**
     * Создаёет значёк
     * @returns {HTMLElement}
     */
    createSpanBadge () {
        let classList = ['d-none', 'col-1', 'offset-1', 'badge', 'rounded-pill', 'text-bg-success', 'fs-6'];
        return this.createHTMLElement('span', classList, {}, 'OK');
    }

    /**
     * Создаёт элемент HTML
     * @param {String} tagName Наименование тэга
     * @param {Array} classList список классов
     * @param {Object} atrs объект с аттрибутами
     * @param {String} text текст
     * @returns {HTMLElement}
     */
    createHTMLElement(tagName, classList, attrs=undefined, text=undefined) {
        let element = document.createElement(tagName);
        for (const list of classList)
            element.classList.add(list);
        if (attrs != undefined)
            for (let key in attrs)
                element.setAttribute(key, attrs[key]);
        if (text != undefined) 
            element.innerText = text;
        return element;
    }
}