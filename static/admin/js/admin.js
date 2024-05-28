try {
    document.querySelector('.main-footer div.float-right').remove()
} catch (e) {
}

try {
    // Ajustar automáticamente la altura del textarea
    function ajustarAlturaTextarea(elemento) {
        elemento.style.height = "auto"; // Restablecer la altura a "auto" para calcular correctamente el nuevo tamaño
        elemento.style.height = (elemento.scrollHeight + 2) + "px"; // Ajustar la altura según el contenido
    }

    document.querySelectorAll("textarea").forEach(e => {
        e.addEventListener("input", function () {
            ajustarAlturaTextarea(this);
        })
    });
} catch (e) {
}


