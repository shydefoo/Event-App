$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type: "POST",
            url: "/api/search_event/",
            data: {
                "search_text": $('#search').val(),
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR){
    $('#search-results').html(data);
}