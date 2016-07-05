/**
 * Created by Lenovo on 2016/7/2.
 */
//var myForm = $('#login_form').submit(function() {
//    $.ajax({
//        url:'auth',
//        type:'post',
//        dataType:'form-data',
//        data:myForm.serializeArray(),
//        success:function(msg) {
//        }
//    });
//    $.post('',{
//        name : $('#swew').val(),
//
//    },function(result){});
//})
$('#addStuBtn').click(function(){
    $.post('/manage/addStudent', {
        name : $('#StudentName').val(),
        studentno : $('#StudentNo').val(),
        phonenumber : $('#StudentTel').val(),
        studentemail : $('#StudentEmail').val(),
        address : $('#StudentAdd').val()
    }, function(result){
        if(result.status == 1) {
            alert('出错');
            location.reload();
        } else if(result.status == 0){
            alert('成功');
            location.reload();
        }
    });
});


$('.deleteStuBtn').click(function(){
    var id = $(this).attr('data-id');
    $('#sureDeleteStu').onclick(function(){
        $.post('/manage/deleteStudent/' + id,
            {},
            function(result){
                if(result.status == 1) {
                    alert('出错');
                    location.reload();
                } else if(result.status == 0){
                    alert('成功');
                    location.reload();
                }
            });
    });
});
//var editStuBtn = $('.editStuBtn');
//editStuBtn.each(function(i) {
//    $(this).click(function() {
//        var name = $(this).parent().parent().find('td').eq(0).html();
//        $("#editStudentNo").val(name);
//    })
//})

var editStuBtn = $('.editStuBtn');
editStuBtn.each(function() {
    $(this).click(function(){
        var sno = $(this).parent().parent().find('td').eq(0).html();
        $("#editStudentNo").val(sno);
        var name = $(this).parent().parent().find('td').eq(1).html();
        $("#editStudentName").val(name);
        var phone = $(this).parent().parent().find('td').eq(2).html();
        $("#editStudentTel").val(phone);
        var email = $(this).parent().parent().find('td').eq(3).html();
        $("#editStudentEmail").val(email);
        var address = $(this).parent().parent().find('td').eq(4).html();
        $("#editStudentAdd").val(address);
        var id = $(this).attr('data-id');
        $('#sureEditStu').click(function(e){
            $.post('/manage/editStudent/' + id, {
                name : $('#editStudentName').val(),
                studentno : $('#editStudentNo').val(),
                phonenumber : $('#editStudentTel').val(),
                studentemail : $('#editStudentEmail').val(),
                address : $('#editStudentAdd').val()
            }, function(result){
                if(result.status == 1) {
                    alert('出错');
                    location.reload();
                } else if(result.status == 0){
                    alert('成功');
                    location.reload();
                }
            });
            return false;
        })
    });
});


$('.search').click(function(){
    $('#searchList').html('');
    $.post('/search', {
        search : $('#search').val()
    }, function(result){
        if(result.status == 0 && result.body != null) {
            for(var i = 0;i<result.body.length;i++) {
                $('#searchList').append('<li class="list-group-item">学号:<p class="list-group-item-text" id="sno">' + result.body[i].sno +'</p></li>' +
                '<li class="list-group-item">姓名:<p class="list-group-item-text" id="sname">' + result.body[i].sname +'</p></li>' +
                '<li class="list-group-item">电话:<p class="list-group-item-text" id="sphone">' + result.body[i].sphone + '</p></li>' +
                '<li class="list-group-item">邮箱:<p class="list-group-item-text" id="semail">' + result.body[i].semail + '</p></li>' +
                '<li class="list-group-item">家庭住址:<p class="list-group-item-text" id="saddress">' + result.body[i].param1 + '</p></li><br>')
            }
            $('#searchResultModal').modal()
        }
        else if(result.status == 0 && result.body == null) {
            $('#noSearchResultModal').modal()
        }
        else {
            $('#searchText').html("查询错误。 <br>请检查是否输入了姓名或学号或输入的姓名或学号有误。")
            $('#noSearchResultModal').modal()
        }
    })
});

