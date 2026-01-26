/**
 * Accordion - модуль для создания аккордеонов с анимацией
 * @class
 * @example
 * // HTML
 * <div class="accordion" data-accordion>
 *   <div data-accordion-item>
 *     <button data-accordion-title>Заголовок</button>
 *     <div data-accordion-content>Контент</div>
 *   </div>
 * </div>
 *
 * // JavaScript
 * import Accordion from './accordion.js';
 * const accordion = new Accordion('.accordion', { duration: 500 });
 * accordion.init();
 */

export default class Accordion {
    /**
     * Константы и дефолтные настройки
     * @type {{duration: number, startActive: boolean, animatePadding: boolean, easing: string, onlyOneOpen: boolean}}
     */
    static defaultOptions = {
        duration: 300,
        easing: 'ease-in-out',
        onlyOneOpen: true,
        startActive: true
    };

    /**
     * Конструктор класса
     * @param {string|HTMLElement} element - Селектор или DOM элемент
     * @param {Object} options - Настройки аккордеона
     */
    constructor(element, options = {}) {
        this.element = this._getElement(element);

        if (!this.element) {
            console.warn('Accordion: элемент не найден', element);
            return;
        }

        this.options = {
            ...Accordion.defaultOptions,
            ...options
        };

        this.items = [];

        this.initialized = false;

        console.log('Accordion: создан экземпляр', this);
    }

    /**
     * Получаем DOM элемент из селектора или готового элемента
     * @private
     */
    _getElement(element) {
        if (typeof element === 'string') {
            return document.querySelector(element);
        }
        return element;
    }

    /**
     *
     */
    _setupItem(item) {
        console.log('Accordion: настраиваю элемент', item);

        const title = item.querySelector('[data-accordion-title]');
        const content = item.querySelector('[data-accordion-content]');

        if (!title || !content) {
            console.warn('Accordion: в элементе не найдены title или content', item);
            return;
        }

        console.log('Accordion: найдены:', { title, content });

        const itemId = `accordion-${Math.random().toString(36).substring(2, 9)}`;

        const itemData = {
            element: item,
            title: title,
            content: content,
            isOpen: item.classList.contains('is-active'),
            id: itemId,
            customPadding: content.dataset.accordionPadding
        };

        this._setupAriaAttributes(itemData);
        
        this._saveOriginalDimensions(itemData);
        
        this._setInitialHeight(itemData);

        this._addClickHandler(itemData);

        this.items.push(itemData);

        console.log('Accordion: элемент настроен', itemData);
    }

    /**
     * Инициализация аккордеона
     */
    init() {
        // Если уже инициализирован - выходим
        if (this.initialized) {
            console.warn('Accordion: уже инициализирован');
            return;
        }

        // Если элемент не найден - выходим
        if (!this.element) {
            console.warn('Accordion: элемент для инициализации не найден');
            return;
        }

        console.log('Accordion: начинаю инициализацию...');
        const itemElements = this.element.querySelectorAll('[data-accordion-item]');

        if (itemElements.length === 0) {
            console.warn('Accordion: не найдены элементы data-accordion-item');
            this.initialized = false;
            return;
        }

        console.log(`Accordion: найдено ${itemElements.length} элементов`);

        itemElements.forEach(item => {
            this._setupItem(item);
        });

        this.initialized = true;
        console.log('Accordion: инициализация завершена');
    }

    _setupAriaAttributes(item) {
        const { title, content, id, isOpen } = item;

        title.setAttribute('id', `${id}-title`);
        title.setAttribute('aria-expanded', isOpen.toString());
        title.setAttribute('aria-controls', `${id}-content`);
        title.setAttribute('role', 'button');

        if (title.tagName !== 'BUTTON') {
            title.setAttribute('tabindex', '0');
        }

        content.setAttribute('id', `${id}-content`);
        content.setAttribute('aria-labelledby', `${id}-title`);
        content.setAttribute('aria-hidden', (!isOpen).toString());
        content.setAttribute('role', 'region');

        console.log('Accordion: ARIA атрибуты установлены для', id);
    }

    /**
     * Сохраняет оригинальные размеры контента
     * @param item
     * @private
     */
    _saveOriginalDimensions(item) {
        const { content, customPadding, isOpen } = item;
        const computedStyle = window.getComputedStyle(content);

        if (customPadding) {
            const clone = content.cloneNode(true);
            clone.style.height = 'auto';
            clone.style.paddingTop = customPadding;
            clone.style.paddingLeft = customPadding;
            clone.style.paddingBottom = customPadding;
            clone.style.paddingRight = customPadding;
            clone.style.visibility = 'hidden';
            clone.style.position = 'absolute';
            clone.style.top = '-9999px';
            clone.style.left = '-9999px';

            clone.style.boxSizing = 'box-sizing';
            document.body.appendChild(clone);
            item.originalHeight = clone.scrollHeight;
            document.body.removeChild(clone);

        } else {
            // Сохраняем полную высоту контента
            item.originalHeight = content.scrollHeight; // Вся высота содержимого
        }

        // Если есть кастомный padding - используем его
        const paddingTop = customPadding || computedStyle.paddingTop;
        const paddingRight = customPadding || computedStyle.paddingRight;
        const paddingBottom = customPadding || computedStyle.paddingBottom;
        const paddingLeft = customPadding || computedStyle.paddingLeft;

        // Сохраняем стили которые влияют на высоту
        item.originalStyles = {
            paddingTop: paddingTop,
            paddingRight: paddingRight,
            paddingBottom: paddingBottom,
            paddingLeft: paddingLeft,
            boxSizing: computedStyle.boxSizing
        };

        console.log('Accordion: сохранены размеры для', item.id, {
            height: item.originalHeight,
            style: item.originalStyles,
            customPadding: customPadding ? 'да' : 'нет'
        });
    }

    /**
     * Устанавливает начальную высоту контента
     * @param item
     * @private
     */
    _setInitialHeight(item) {
        const { content, isOpen, originalStyles } = item;

        // Устанавливаем CSS transition для плавности
        content.style.transition = `
            height ${this.options.duration}ms ${this.options.easing},
            padding-top ${this.options.duration}ms ${this.options.easing},
            padding-bottom ${this.options.duration}ms ${this.options.easing}
        `;
        content.style.overflow = 'hidden'; // Скрываем то, что выходит за пределы
        content.style.paddingRight = originalStyles.paddingRight;
        content.style.paddingLeft = originalStyles.paddingLeft;
        content.style.boxSizing = originalStyles.boxSizing;

        if (isOpen) {
            // Если открыт - устанавливаем полную высоту
            content.style.height = `${item.originalHeight}px`;
            content.style.paddingTop = originalStyles.paddingTop;
            content.style.paddingBottom = originalStyles.paddingBottom;
        } else {
            // Если закрыт - высота 0
            content.style.height = '0';
            content.style.paddingTop = '0';
            content.style.paddingBottom = '0';
        }

        console.log('Accordion: установлена начальная высота для', item.id,
            isOpen ? 'открыт' : 'закрыт');
    }

    /**
     * Добавляет обработчик клика на заголовок
     * @param item
     * @private
     */
    _addClickHandler(item) {
        const { title } = item;

        // Сохраняем контекст this
        const self = this;

        // Создаем функцию-обработчик
        const clickHandler = function(event) {
            event.preventDefault();
            console.log('Accordion: клик по', item.id);

            // Переключаем состояние этого элемента
            self._toggleItem(item);
        };

        // Сохраняем ссылку на обработчик для возможности удаления
        item.clickHandler = clickHandler;

        // Вешаем обработчик
        title.addEventListener('click', clickHandler);

        // Также обрабатываем нажатие клавиши Enter/Space для доступности
        title.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                clickHandler(event);
            }
        });

        console.log('Accordion: обработчик добавлен для', item.id);

    }

    /**
     * Переключает состояние элемента (открыть/закрыть)
     * @param item
     * @private
     */
    _toggleItem(item) {
        console.log('Accordion: переключаю', item.id, 'текущее состояние:', item.isOpen ? 'открыт' : 'закрыт');

        // Если опция onlyOneOpen: true - закрываем другие элементы
        if (this.options.onlyOneOpen && !item.isOpen) {
            this._closeOtherItems(item);
        }

        // Определяем нужно открыть или закрыть
        if (item.isOpen) {
            this._closeItem(item);
        } else {
            this._openItem(item);
        }

        // Меняем состояние в памяти
        item.isOpen = !item.isOpen;

        // Обновляем CSS классы
        this._updateItemClasses(item);

        // Обновляем ARIA атрибуты
        this._updateAriaAttributes(item);

        console.log('Accordion: новое состояние:', item.isOpen ? 'открыт' : 'закрыт');
    }

    /**
     * Закрывает все другие элементы (если onlyOneOpen: true)
     * @param currentItem
     * @private
     */
    _closeOtherItems(currentItem) {
        this.items.forEach(otherItem => {
            // Пропускаем текущий элемент и уже закрытые
            if (otherItem === currentItem || !otherItem.isOpen) {
                return;
            }

            console.log('Accordion: закрываю другой элемент', otherItem.id);

            // Закрываем элемент
            this._closeItem(otherItem);
            otherItem.isOpen = false;
            this._updateItemClasses(otherItem);
            this._updateAriaAttributes(otherItem);
        });
    }

    /**
     * Открывает элемент с анимацией
     * @param item
     * @private
     */
    _openItem(item) {
        const { content, originalHeight, originalStyles } = item;

        console.log('Accordion: открываю', item.id, 'до высоты', originalHeight);

        // Сначала устанавливаем точную высоту (чтобы анимация работала от 0 до этой высоты)
        content.style.height = `${originalHeight}px`;

        // Если нужно анимировать padding (опционально)
        if (originalStyles.paddingTop && originalStyles.paddingBottom) {
            content.style.paddingTop = originalStyles.paddingTop;
            content.style.paddingBottom = originalStyles.paddingBottom;
        }
    }

    /**
     * Закрывает элемент с анимацией
     * @param item
     * @private
     */
    _closeItem(item) {
        const { content, originalStyles } = item;

        console.log('Accordion: закрываю', item.id);

        // Устанавливаем высоту 0 для анимации закрытия
        content.style.height = '0';

        // Если анимируем padding - тоже устанавливаем в 0
        if (originalStyles.paddingTop && originalStyles.paddingBottom) {
            content.style.paddingTop = '0';
            content.style.paddingBottom = '0';
        }
    }

    /**
     * Обновляет ARIA атрибуты после изменения состояния
     * @param item
     * @private
     */
    _updateAriaAttributes(item) {
        const { title, content, isOpen } = item;

        // Обновляем заголовок
        title.setAttribute('aria-expanded', isOpen.toString());

        // Обновляем контент
        content.setAttribute('aria-hidden', (!isOpen).toString());

        console.log('Accordion: ARIA обновлены для', item.id, 'isOpen:', isOpen);
    }

    /**
     * Обновляет CSS классы элемента после изменения состояния
     * @param item
     * @private
     */
    _updateItemClasses(item) {
        const { element, isOpen } = item;

        if (isOpen) {
            element.classList.add('is-active');
        } else {
            element.classList.remove('is-active');
        }

        console.log('Accordion: классы обновлены для', item.id,
            'is-active:', isOpen);
    }
    /**
     * Открывает конкретный элемент по индексу
     * @param {number} index - Индекс элемента в массиве items
     */
    open(index) {
        if (!this.initialized) {
            console.warn('Accordion: не инициализирован');
            return;
        }

        if (index < 0 || index >= this.items.length) {
            console.warn('Accordion: неверный индекс', index);
            return;
        }

        const item = this.items[index];
        console.log('Accordion: открываю элемент по индексу', index, item.id);

        if (!item.isOpen) {
            this._toggleItem(item);
        }
    }

    /**
     * Закрывает конкретный элемент по индексу
     * @param {number} index - Индекс элемента в массиве items
     */
    close(index) {
        if (!this.initialized) {
            console.warn('Accordion: не инициализирован');
            return;
        }

        if (index < 0 || index >= this.items.length) {
            console.warn('Accordion: неверный индекс', index);
            return;
        }

        const item = this.items[index];
        console.log('Accordion: закрываю элемент по индексу', index, item.id);

        if (item.isOpen) {
            this._toggleItem(item);
        }
    }

    /**
     * Открывает все элементы
     */
    openAll() {
        if (!this.initialized) {
            console.warn('Accordion: не инициализирован');
            return;
        }

        console.log('Accordion: открываю все элементы');

        // Временно отключаем onlyOneOpen
        const originalSettings = this.options.onlyOneOpen;
        this.options.onlyOneOpen = false;

        // Открываем все закрытые элементы
        this.items.forEach((item, index) => {
            if (!item.isOpen) {
                this._toggleItem(item);
            }
        });

        // Восстанавливаем настройку
        this.options.onlyOneOpen = originalSettings;
    }

    /**
     * Закрывает все элементы
     */
    closeAll() {
        if (!this.initialized) {
            console.warn('Accordion: не инициализирован');
            return;
        }

        console.log('Accordion: закрываю все элементы');

        // Закрываем все открытые элементы
        this.items.forEach((item, index) => {
            if (item.isOpen) {
                this._toggleItem(item);
            }
        });
    }

    /**
     * Возвращает текущее состояние элемента
     * @param {number} index - Индекс элемента
     * @returns {boolean} true если открыт
     */
    isOpen(index) {
        if (!this.initialized || index < 0 || index >= this.items.length) {
            return false;
        }

        return this.items[index].isOpen;
    }

    /**
     * Уничтожает аккордеон, удаляя все обработчики
     */
    destroy() {
        if (!this.initialized) {
            return;
        }

        console.log('Accordion: уничтожаю...');

        // Удаляем все обработчики кликов
        this.items.forEach(item => {
            if (item.clickHandler) {
                item.title.removeEventListener('click', item.clickHandler);
            }

            // Убираем стили
            item.content.style.transition = '';
            item.content.style.height = '';
            item.content.style.overflow = '';

            // Возвращаем стили
            item.content.style.paddingTop = item.originalStyles.paddingTop;
            item.content.style.paddingBottom = item.originalStyles.paddingBottom;
            item.content.style.boxSizing = item.originalStyles.boxSizing;
        });

        // Очищаем массивы
        this.items = [];
        this.initialized = false;

        console.log('Accordion: уничтожен');
    }
}

export function createAccordion(selector, options = {}) {
    const accordion = new Accordion(selector, options);
    accordion.init();
    return accordion;
}