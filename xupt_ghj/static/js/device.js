$('#remote button').click(function (event) {
    var param = {};
    var arr = this.value.split('-');
    param.key = arr[1];
    param.device = arr[0];
    $.ajax({
        url: '/send',
        type: 'post',
        async: false,
        data: param,
        success: function (data) {
            if (data == 'ok') {
                $.message({
                    message: '<br>success!',
                    type: 'success'
                });
            } else {
                $.message({
                    message: '<br>警告:' +
                    '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;参数异常，请稍后再试',
                    type: 'warning'
                });
            }
        },
        error: function (data) {
            $.message({
                message: '<br>发送失败',
                type: 'warning'
            });
        }
    });
});
