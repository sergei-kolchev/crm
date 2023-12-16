function cngElementsAtr(cls, atr, val){
    var elems = document.getElementsByClassName(cls);
    for (var i = 0; i < elems.length; i++) {
        elems[i][atr] = val;
    }
}

document.body.addEventListener('htmx:afterRequest', (event) => {
    path_str = event.detail.pathInfo.requestPath;
    path_str = path_str.split('?')[0]
    if (path_str.includes('create/')) {
        arr = document.getElementsByClassName('error-message');
        if (arr.length == 0) {
              cngElementsAtr('form-control', 'value', '');
        }
    } else if (path_str.includes('update/')) {
        if (event.detail.requestConfig.verb === 'put') {
            cngElementsAtr('disbtn', 'disabled', true);
        } else {
            cngElementsAtr('disbtn', 'disabled', false);
        }
    } else if (path_str.includes('detail/')) {
        cngElementsAtr('disbtn', 'disabled', false);
    } else if (path_str.includes('patients/sort/')) {
            path_arr = path_str.split('/');
            curr_class = path_arr.pop()
            curr_class = path_arr.pop() + '-' + curr_class
            document.getElementsByClassName('disabled-button')[0].classList.remove('disabled-button');
            document.getElementsByClassName(curr_class)[0].classList.add('disabled-button');
    }
});

document.body.addEventListener('"successMessage"', function(evt){
    Swal.fire({
               position: 'top-end',
               icon: 'success',
               title: 'Успешно',
               showConfirmButton: false,
               timer:1500
            });
})

document.body.addEventListener('"errorMessage"', function(evt){
    Swal.fire({
               position: 'top-end',
               icon: 'warning',
               title: 'Ошибка',
               showConfirmButton: false,
               timer:1500
            });
})
