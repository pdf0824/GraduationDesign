$('#STB button').click(function (event) {
    var arr = this.value.split('!');
    var keyName = arr[0];
    var command = arr[1];
    $.ajax({
        type: "GET",
        url: "/studyKey",
        cache: false, //禁用缓存
        data: {'keyName': keyName, 'command': command}, //传入组装的参数
        success: function (result) {
            console.log(result);
            if (result == 'ok') {
                alert('学习完成，测试一下吧！');
            } else {
                alert('补签提交失败！');
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
});