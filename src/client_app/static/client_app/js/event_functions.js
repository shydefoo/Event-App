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
    $('#comment-on-event').on('click', function(){
        console.log('clicked')
        text = $('#id_comment').val()
        if(text != ''){
            $.ajax({
                type: 'POST',
                url: '/api/comment_event/',
                data: {
                    'event_id': event_id,
                    'comment': text,
                },
                success: HandleCommentOnEvent,
                dataType: 'json'
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

function HandleCommentOnEvent(data, textStatus, jqXHR){
    var arr = window.location.pathname.split('/')
    var event_id = arr[arr.length-1]
    $.ajax({
        type: 'GET',
        url: '/api/get_event_comments/'+event_id,
        success: DisplayComments,
        dataType: 'json',
    });
}

function DisplayComments(data, textStatus, jqXHR){
    console.log('display comments');
    var contents = "";
    var obj = jQuery.parseJSON(data)
    $.each(obj, function(inde, jsonObject){
        for (var i=0;i<jsonObject.length;i++){
            contents += "<div class='card'>";
            contents += "<p>User: " + jsonObject[i].username +"</p>";
            contents += "<p>Date: " + jsonObject[i].datetime + "</p>";
            contents += "<p>Comment: "+ jsonObject[i].comment + "<br>";
            contents += "</div>"
        }
    });

    console.log(contents)
    $('#comments').html(contents)
}