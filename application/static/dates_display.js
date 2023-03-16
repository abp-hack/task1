
function f() {
    setTimeout(() => {
        for (var i = 0; i < 30; ++i) {
            el = document.getElementById(`id_numbers-${i}-status`);
            console.log(el.options[el.selectedIndex].text)
            if (el.options[el.selectedIndex].text == 'Свободен (чистый)' || el.options[el.selectedIndex].text == 'Свободен (грязный)') {
                document.getElementById(`id_numbers-${i}-date_started`).parentElement.style = 'opacity: 0;'
                document.getElementById(`id_numbers-${i}-date_end`).parentElement.style = 'opacity: 0;'
            } else {
                document.getElementById(`id_numbers-${i}-date_started`).parentElement.style = 'opacity: 1;'
                document.getElementById(`id_numbers-${i}-date_end`).parentElement.style = 'opacity: 1;'

            }
            addEventListener('click', f)
        }
    }, 100)
}
setTimeout(() => {f()}, 500)