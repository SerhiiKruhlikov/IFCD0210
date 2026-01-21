const objetivo = Math.floor(Math.random() * 100);
const intentos = 10;

const resultado = document.getElementById("resultado");
const quedan = document.getElementById("quedan");
const input = document.getElementById("numero");
const reinicio = document.createElement("button");
reinicio.setAttribute("onclick", "location.reload();");
reinicio.innerText = "¡Inténtalo de nuevo!";
reinicio.className = "reinicio";

let intentos_usuario = 10;

function adivinar(form) {
    event.preventDefault();

    if (intentos_usuario === 0) {
        resultado.parentNode.append(reinicio);
        return;
    }

    let numero = form.querySelector('input').value * 1;
    let div = document.createElement("div");

    --intentos_usuario;

    // ¡Inténtalo de nuevo!

    if (numero === objetivo) {
        div.innerText = `¡Felicidades, han adivinado el número ${numero}!`;
        div.className = "felicidades";
        intentos_usuario = 0;

        input.disabled = true;

        reinicio.innerText = "¿Quieren jugar otra vez?";
        resultado.parentNode.append(reinicio);
    } else {
        if (numero < objetivo) {
            div.innerText = `El número ${numero} es menor que el objetivo.`;
        } else {
            div.innerText = `El número ${numero} es mayor que el objetivo.`;
        }

    }

    console.log(objetivo);



    quedan.innerText = intentos_usuario;
    resultado.prepend(div);
    form.reset();
}
