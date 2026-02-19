export default class Navbar {

    static defaultOptions = {
        duration: 300,
        easing: 'ease-in-out',
        onlyOneOpen: true,
        startActive: true
    };

    constructor(element, options = {}) {
        this.element = this._getElement(element);

        if (!this.element) {
            console.warn('Navbar: элемент не найден', element);
            return;
        }

        this.options = {
            ...Navbar.defaultOptions,
            ...options
        };

        this.items = [];

        this.navbarId = `navbar-${Math.random().toString(36).substring(2, 9)}`;

        this.panel = '';

        this.toggle = ''

        this.initialized = false;

        console.log('Navbar: создан экземпляр', this);
    }

    _getElement(element) {
        if (typeof element === 'string') {
            return document.querySelector(element);
        }
        return element;
    }

    init() {
        // Если уже инициализирован - выходим
        if (this.initialized) {
            console.warn('Navbar: уже инициализирован');
            return;
        }

        // Если элемент не найден - выходим
        if (!this.element) {
            console.warn('Navbar: элемент для инициализации не найден');
            return;
        }

        console.log('Navbar: начинаю инициализацию...');
        const navbarToggle = this.element.querySelector('[data-navbar-toggle]');
        const navbarPanel = this.element.querySelector('[data-navbar-panel]');

        if (navbarToggle.length === 0) {
            console.warn('Navbar: не найден элемент data-navbar-toggle');
            this.initialized = false;
            return;
        }

        if (navbarPanel.length === 0) {
            console.warn('Navbar: не найден элемент data-navbar-panel');
            this.initialized = false;
            return;
        }

        console.log(`Navbar: найден ${navbarToggle.length} элемент`);
        this._setupToggle(navbarToggle);

        console.log(`Navbar: найден ${navbarPanel.length} элемент`);
        this._setupPanel(navbarPanel);

        this.initialized = true;
        console.log('Navbar: инициализация завершена');
    }

    _setupToggle(element) {
        console.log('Navbar: настраиваю переключатель', element);

        const elementId = `navbar-${Math.random().toString(36).substring(2, 9)}`;

        const elementData = {
            element: element,
            toggle: true,
            panel: false,
            isOpen: element.classList.contains('is-active'),
            id: this.navbarId
        }

        this._setupAriaAttributes(elementData);

        this._addClickHandler(elementData);

        this.toggle = elementData;

        console.log('Navbar: переключатель настроен', elementData);
    }

    _setupPanel(element) {
        console.log('Navbar: настраиваю панель', element);

        const elementId = `navbar-${Math.random().toString(36).substring(2, 9)}`;

        const elementData = {
            element: element,
            toggle: false,
            panel: true,
            isOpen: element.classList.contains('is-active'),
            id: this.navbarId
        }

        this._setupAriaAttributes(elementData);

        this.panel = elementData;

        console.log('Navbar: элемент настроен', elementData);
    }

    _setupAriaAttributes(data) {
        const { element, toggle, panel, isOpen, id } = data;

        if (toggle) {
            element.setAttribute('id', `${id}-toggle`);
            element.setAttribute('aria-expanded', isOpen.toString());
            element.setAttribute('aria-controls', `${id}-panel`);
            element.setAttribute('role', 'button');
        }

        if (panel) {
            element.setAttribute('id', `${id}-panel`);
            element.setAttribute('aria-labelledby', `${id}-toggle`);
            element.setAttribute('aria-hidden', (!isOpen).toString());
            element.setAttribute('role', 'region');
        }

        console.log('Navbar: ARIA атрибуты установлены для', element);
    }

    _addClickHandler(item) {
        const { element, toggle } = item;

        console.log(element);
        console.log(item);

        const self = this;

        const clickHandler = function(event) {
            event.preventDefault();
            console.log('Navbar: клик по', item.id);

            // Переключаем состояние этого элемента
            self._toggleItem(element);
        };

        item.clickHandler = clickHandler;

        element.addEventListener('click', clickHandler);

        element.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                clickHandler(event);
            }
        });

        console.log('Navbar: обработчик добавлен для', item.id);
    }

    open(element) {
        if (!this.initialized) {
            console.warn('Navbar: не инициализирован');
            return;
        }

        if (element < 0 || element >= this.panel.length) {
            console.warn('Navbar: неверный элемент', element);
            return;
        }
    }

    _toggleItem(item) {
        console.log(item);
        console.log('Navbar: переключаю', item.id, 'текущее состояние:', item.isOpen ? 'открыт' : 'закрыт');

        if (item.isOpen) {
            this._closeItem(item);
        } else {
            this._openItem(item);
        }

        item.isOpen = !item.isOpen;

        this._updateItemClasses(item);

        this._updateAriaAttributes(item);

        console.log('Accordion: новое состояние:', item.isOpen ? 'открыт' : 'закрыт');
    }

    _openItem(item) {
        console.log(item);

        console.log('Navbar: открываю', item.id);

        content.style.height = 'auto';
    }

    _closeItem(item) {
        console.log(item);

        console.log('Navbar: закрываю', item.id);

        content.style.height = '0';
    }
}

export function createNavbar(selector, options = {}) {
    const navbar = new Navbar(selector, options);
    navbar.init();
    return navbar;
}