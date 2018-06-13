function delDevice(data) {
    $.confirm({
        title: '确定删除?',
        content: '<br>删除之后将不能再找回!',
        type: 'red',
        buttons: {
            ok: {
                text: "ok!",
                btnClass: 'btn-primary',
                keys: ['enter'],
                action: function () {
                    var url = 'url:/name.del?id=' + data;
                    ajax(url, 'delete ok!')
                }
            },
            cancel: function () {
                console.log('the user clicked cancel');
            }
        }
    });
}

function naming(id) {
    $.confirm({
        title: 'Rename!',
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>Enter something here</label>' +
        '<input type="text" placeholder="Device name" class="name form-control" required />' +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    var name = this.$content.find('.name').val();
                    if (!name) {
                        $.alert('provide a valid name');
                        return false;
                    }
                    var url = 'url:/name.change?name=' + name + '&id=' + id;
                    ajax(url, 'change device name success!')
                }
            },
            cancel: function () {
                //close
            }
        }
    });
}

function ajax(url, contend) {
    $.confirm({
            title: "Successful!",
            type: 'green',
        content: url,
        contentLoaded: function (data, status, xhr) {
            if (status == 'error') {
                this.close();
                $.confirm({
                    title: 'Error',
                    content: 'Some error occur!<br>Please try again later!',
                    type: 'red',
                    buttons: {
                        ok: function () {

                        }
                    }
                })
            } else if (data == 'ok') {
                this.setContentAppend('<br>Status: ' + contend);
            } else {
                this.close();
                $.confirm({
                    title: 'Exception',
                    content: 'A Exception occur:<br>' + data + '<br>Please try again later!',
                    type: 'red',
                    buttons: {
                        ok: function () {

                        }
                    }
                })
            }

        },
        buttons: {
            ok: function () {
                window.location.reload();
                console.log('suc');
            }
        }
    });
}