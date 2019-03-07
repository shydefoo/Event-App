$(function () {
    $('#participate').on('click', function () {
        var arr = window.location.pathname.split('/')
        var event_id = arr[arr.length-1]
        console.log('test' + event_id)
        var Status = $(this).val();
        $.ajax({
            type: "POST",
            url: '/api/join_event/',
            data: {
                'event_id':event_id,
            },
            success: HandleResponse,
            dataType : 'json',
        });
    });
});

function HandleResponse(data, textStatus, jqXHR){

}