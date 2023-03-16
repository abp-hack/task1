
function f() {
    setTimeout(() => {
        try {
            var element = document.getElementById('id_tel');
            var maskOptions = {
                mask: '+{7}(900) 000-00-00'
            };
            IMask(element, maskOptions);
        } catch {}
        for (var i = 0; i < 100; ++i) {
            var el = document.getElementById(`id_clients-${i}-tel`);
            console.log(el)
            var maskOptions = {
                mask: '+{7}(900) 000-00-00'
            };
            IMask(el, maskOptions);
        }
    }, 1000)
}

addEventListener('click', f)
f()