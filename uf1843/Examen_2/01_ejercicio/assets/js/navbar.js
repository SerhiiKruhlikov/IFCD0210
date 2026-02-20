export default class Navbar {
    static defaultOptions = {
        duration: 300,
        easing: 'ease-in-out',
        startActive: false
    };

    constructor(element, options = {}) {
        this.element = this._getElement(element);

        if (!this.element) {
            // console.warn('Navbar: elemento no encontrado', element);
            return;
        }

        this.options = {
            ...Navbar.defaultOptions,
            ...options
        };

        this.toggler = null;
        this.panel = null;
        this.isOpen = false;
        this.initialized = false;
        this.isAnimating = false;
        this.resizeObserver = null;
        this.boundHandleResize = this._handleResize.bind(this);
    }

    _getElement(element) {
        if (typeof element === 'string') {
            return document.querySelector(element);
        }
        return element;
    }

    _isTogglerVisible() {
        if (!this.toggler) return false;
        const style = window.getComputedStyle(this.toggler);
        return style.display !== 'none';
    }

    init() {
        if (this.initialized) return;
        if (!this.element) return;

        const toggler = this.element.querySelector('[data-navbar-toggle]');
        const panel = this.element.querySelector('[data-navbar-panel]');

        if (!toggler || !panel) {
            // console.warn('Navbar: no se encontraron los elementos necesarios');
            return;
        }

        this.toggler = toggler;
        this.panel = panel;

        this._watchVisibility();
        this._applyVisibilityState();
    }

    _watchVisibility() {
        this.resizeObserver = new ResizeObserver(() => {
            this._applyVisibilityState();
        });

        this.resizeObserver.observe(this.toggler);
        window.addEventListener('resize', this.boundHandleResize);
    }

    _applyVisibilityState() {
        const isVisible = this._isTogglerVisible();

        if (!isVisible) {
            // console.log('Navbar: botón oculto, el panel siempre está visible');
            this._enableDesktopMode();
        } else {
            // console.log('Navbar: botón visible, activando modo móvil');
            this._enableMobileMode();
        }
    }

    _enableDesktopMode() {
        this.panel.style.height = '';
        this.panel.style.overflow = '';
        this.panel.style.transition = '';

        this.panel.classList.remove('is-active');
        this.toggler.classList.remove('is-active');

        this.panel.style.display = '';

        if (this.initialized) {
            this._removeEventListeners();
            this.initialized = false;
        }

        // console.log('Navbar: modo escritorio activado');
    }

    _enableMobileMode() {
        this.panel.style.display = '';

        if (!this.initialized) {
            this._initialize();
        }
    }

    _initialize() {
        this._preparePanel();

        this.isOpen = this.options.startActive;

        if (this.isOpen) {
            this.toggler.classList.add('is-active');
            this.panel.classList.add('is-active');
            this.panel.style.height = 'auto';
        } else {
            this.panel.style.height = '0';
        }

        this._setupAriaAttributes();
        this._addEventListeners();

        this.initialized = true;
        // console.log('Navbar: modo móvil inicializado');
    }

    _handleResize() {
        this._applyVisibilityState();
    }

    _preparePanel() {
        this.panel.style.overflow = 'hidden';
        this.panel.style.transition = `height ${this.options.duration}ms ${this.options.easing}`;
        this.panel.style.display = '';
    }

    _setupAriaAttributes() {
        const navbarId = this.element.id || `navbar-${Math.random().toString(36).substring(2, 9)}`;
        this.element.id = navbarId;

        this.toggler.setAttribute('aria-expanded', this.isOpen.toString());
        this.toggler.setAttribute('aria-controls', `${navbarId}-panel`);
        this.toggler.setAttribute('role', 'button');

        this.panel.id = `${navbarId}-panel`;
        this.panel.setAttribute('aria-labelledby', this.toggler.id || `${navbarId}-toggle`);
        this.panel.setAttribute('aria-hidden', (!this.isOpen).toString());
        this.panel.setAttribute('role', 'region');

        if (!this.toggler.id) {
            this.toggler.id = `${navbarId}-toggle`;
        }
    }

    _addEventListeners() {
        this.boundToggle = (e) => {
            e.preventDefault();
            this.toggle();
        };

        this.boundKeydown = (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggle();
            }
        };

        this.boundTransitionEnd = () => {
            this.isAnimating = false;
            if (this.isOpen) {
                this.panel.style.height = 'auto';
            }
        };

        this.toggler.addEventListener('click', this.boundToggle);
        this.toggler.addEventListener('keydown', this.boundKeydown);
        this.panel.addEventListener('transitionend', this.boundTransitionEnd);
    }

    _removeEventListeners() {
        if (this.boundToggle) {
            this.toggler.removeEventListener('click', this.boundToggle);
        }
        if (this.boundKeydown) {
            this.toggler.removeEventListener('keydown', this.boundKeydown);
        }
        if (this.boundTransitionEnd) {
            this.panel.removeEventListener('transitionend', this.boundTransitionEnd);
        }
    }

    toggle() {
        if (this.isAnimating || !this.initialized) return;
        this.isAnimating = true;

        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        if (this.isOpen) {
            this.isAnimating = false;
            return;
        }

        const startHeight = '0';

        this.panel.style.height = 'auto';
        const endHeight = this.panel.scrollHeight + 'px';

        this.panel.style.height = startHeight;

        setTimeout(() => {
            this.panel.style.height = endHeight;
        }, 10);

        this.isOpen = true;
        this._updateState();
        // console.log('Navbar: panel abriéndose');
    }

    close() {
        if (!this.isOpen) {
            this.isAnimating = false;
            return;
        }

        if (this.panel.style.height === 'auto') {
            const currentHeight = this.panel.scrollHeight + 'px';
            this.panel.style.height = currentHeight;
        }

        setTimeout(() => {
            this.panel.style.height = '0';
        }, 10);

        this.isOpen = false;
        this._updateState();
        // console.log('Navbar: panel cerrándose');
    }

    _updateState() {
        this.toggler.classList.toggle('is-active', this.isOpen);
        this.panel.classList.toggle('is-active', this.isOpen);

        this.toggler.setAttribute('aria-expanded', this.isOpen.toString());
        this.panel.setAttribute('aria-hidden', (!this.isOpen).toString());
    }

    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        window.removeEventListener('resize', this.boundHandleResize);
        this._removeEventListeners();
    }
}

export function createNavbar(selector, options = {}) {
    const navbar = new Navbar(selector, options);
    navbar.init();
    return navbar;
}