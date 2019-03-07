$(function () {
    var arr = window.location.pathname.split('/')
    var event_id = arr[arr.length-1]
    $('#join').on('click', function () {
        if($('#join').val() =='join'){
            $.ajax({
                type: "POST",
                url: '/api/join_event/',
                data: {
                    'event_id':event_id,
                },
                success: handleParticipateResponse,
                dataType : 'json',
            });
        }
        else if($('#join').val() == 'leave'){
            $.ajax({
                type: "POST",
                url: '/api/leave_event/',
                data: {
                    'event_id':event_id,
                },
                success: HandleUnparticipateResponse,
                dataType : 'json',
            });
        }

    });

    $('#like').on('click', function(){
        if($('#like').val() == 'like'){
            $.ajax({
                type: "POST",
                url: "/api/like_event/",
                data: {
                    'event_id': event_id
                },
                success: HandleLikeResponse,
                dataType:'json',
            });
        }
        if($('#like').val() == 'dislike'){
            $.ajax({
                type: "POST",
                url: "/api/dislike_event/",
                data: {
                    'event_id': event_id
                },
                success: HandleDisikeResponse,
                dataType:'json',
            });
        }

    });
});

function handleParticipateResponse(data, textStatus, jqXHR){
//    console.log('joined event!');
    $('#join').val("leave");
    $('#join').html('Leave Event');
    console.log('joined event!');
}

function HandleUnparticipateResponse(data, textStatus, jqXHR){
    $('#join').val('join');
    $('#join').html('Join Event');
}


function HandleLikeResponse(data, textStatus, jqXHR){
    console.log('data: '+ data)
    $('#like').val('dislike')
    $('#like').html('Dislike Event')
}

function HandleDisikeResponse(data, textStatus, jqXHR){
    console.log('data: '+ data)
    $('#like').val('like')
    $('#like').html('Like Event')
}
