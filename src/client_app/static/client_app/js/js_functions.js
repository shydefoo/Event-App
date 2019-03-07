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
    if($('#search').val()==0){
        console.log('empty')
        $('#search-results').empty();
    }
});

function searchSuccess(data, textStatus, jqXHR){
    $('#search-results').html(data);
}