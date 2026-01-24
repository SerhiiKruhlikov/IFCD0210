const box = document.querySelectorAll('[data-tab-content]')[0];
const button = document.getElementById('toggleBtn');

const originalScrollHeight = box.scrollHeight;

const computedStyle = window.getComputedStyle(box);
const originalPaddingTop = computedStyle.paddingTop;
const originalPaddingBottom = computedStyle.paddingBottom

const settings = {
    duration: 500, // время анимации в мс
    easing: 'ease-in-out' // тип плавности
};

box.style.paddingTop = `${originalPaddingTop}`;
box.style.paddingBottom = `${originalPaddingBottom}`;
box.style.height = `${originalScrollHeight}px`;
box.style.overflow = 'visible';
box.style.transition = `
    height ${settings.duration}ms ${settings.easing},
    padding-top ${settings.duration}ms ${settings.easing},
    padding-bottom ${settings.duration}ms ${settings.easing}
`;

let isOpen = true;

function toggleHeight() {
    if (isOpen) {
        box.style.paddingTop = '0';
        box.style.paddingBottom = '0';
        box.style.height = '0';
        box.style.overflow = 'hidden';
        box.style.transition;
    } else {
        box.style.paddingTop = `${originalPaddingTop}`;
        box.style.paddingBottom = `${originalPaddingBottom}`;
        box.style.height = `${originalScrollHeight}px`;
        box.style.overflow = 'visible';
        box.style.transition;
    }

    isOpen = !isOpen;
}

button.addEventListener('click', toggleHeight);