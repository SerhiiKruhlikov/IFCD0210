console.log('reloj init');

function actualizarTiempo() {
    let fecha = new Date();

    let diasSemana = ['DOM', 'LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB'];

    // Создаем элементы
    let reloj = Object.assign(document.createElement("div"), {className: "reloj"});
    let tiempo = Object.assign(document.createElement("div"), {className: "tiempo"});
    let calendario = Object.assign(document.createElement("div"), {className: "calendario"});
    let dia = Object.assign(document.createElement("span"), {className: "dia"});
    let horas = Object.assign(document.createElement("span"), {className: "horas"});
    let minutos = Object.assign(document.createElement("span"), {className: "minutos"});
    let segundos = Object.assign(document.createElement("span"), {className: "segundos"});
    let dd = Object.assign(document.createElement("span"), {className: "dd"});
    let mm = Object.assign(document.createElement("span"), {className: "mm"});

    // Функция обновления текста
    function actualizarTexto() {
        let fecha = new Date();
        horas.innerText = fecha.getUTCHours().toString().padStart(2, '0');
        minutos.innerText = fecha.getUTCMinutes().toString().padStart(2, '0');
        segundos.innerText = fecha.getUTCSeconds().toString().padStart(2, '0');
        dd.innerText = fecha.getUTCDate().toString().padStart(2, "0");
        month = fecha.getUTCMonth() + 1;
        mm.innerText = month.toString().padStart(2, "0");
        dia.innerText = diasSemana[fecha.getDay()];
    }

    // Инициализируем время
    actualizarTexto();

    // Собираем элементы с двоеточиями
    tiempo.append(horas, ":", minutos, ":", segundos);
    calendario.append(dd, "/", mm);
    reloj.append(tiempo, calendario, dia);

    // Возвращаем созданный элемент
    return reloj;
}

// Создаем часы и добавляем в body
let reloj = actualizarTiempo();
document.getElementsByTagName("main")[0].append(reloj);

// Запускаем обновление каждую секунду
setInterval(() => {
    let fecha = new Date();
    reloj.querySelector('.horas').innerText = fecha.getUTCHours().toString().padStart(2, '0');
    reloj.querySelector('.minutos').innerText = fecha.getUTCMinutes().toString().padStart(2, '0');
    reloj.querySelector('.segundos').innerText = fecha.getUTCSeconds().toString().padStart(2, '0');
}, 1000);