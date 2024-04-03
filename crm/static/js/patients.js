let counter = 0;


function cngElementsAtr(cls, atr, val){
    var elems = document.getElementsByClassName(cls);
    for (var i = 0; i < elems.length; i++) {
        elems[i][atr] = val;
    }
}

function changeElementsStyle(cls, attribute, value) {
    var elems = document.getElementsByClassName(cls);
    for (var i = 0; i < elems.length; i++) {
        elems[i].style.setProperty(attribute, value);
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
    } else if (path_str.includes('sort/')) {
        path_arr = path_str.split('/');
        path_arr.pop()
        curr_class = path_arr.pop()
        curr_class = path_arr.pop() + '-' + curr_class
        document.getElementsByClassName('disabled-button')[0].classList.remove('disabled-button');
        document.getElementsByClassName(curr_class)[0].classList.add('disabled-button');
    }
});

function addEventListener(event_name, icon, title) {
    document.body.addEventListener(event_name, function(evt) {
        Swal.fire({
           position: 'top-end',
           icon: icon,
           title: title,
           showConfirmButton: false,
           timer:1500
        });
    });
}


function pollForResult(url) {
    fetch(url).then(response => response.json())
              .then(response => {
                  if (response['task_status']) {
                        task_status = response['task_status']
                        if (task_status == 'SUCCESS') {
                            changeElementsStyle('waiting', 'display', 'none');
                            changeElementsStyle('finished', 'display', 'block');
                            changeElementsStyle('downloading_error', 'display', 'none');
                            document.body.dispatchEvent(new Event('"successMessage"'));
                        } else {
                            if (counter >= 5){
                                changeElementsStyle('waiting', 'display', 'none');
                                changeElementsStyle('finished', 'display', 'none');
                                changeElementsStyle('downloading_error', 'display', 'block');
                                document.body.dispatchEvent(new Event('"errorMessage"'));
                            } else {
                                counter += 1
                                setTimeout(function(){
                                    pollForResult(url);
                                }, 3000);
                            }
                        }
                  }
    })
}


addEventListener('"successMessage"', 'success', 'Успешно')
addEventListener('"errorMessage"', 'warning', 'Ошибка')
addEventListener('htmx:sendError', 'warning', 'Соединение потеряно')