$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type: "POST",
            url: "/api/search_event/",
            data: {
                "search_text": $('#search').val(),
            },
            success: searchSuccess,
            dataType: 'json'
        });

    });
    if($('#search').val()==0){
        console.log('empty')
        $('#search-results').empty();
    }
});

function searchSuccess(data, textStatus, jqXHR){

    $('#search-results').html(data);
    var contents = "";
    var obj = jQuery.parseJSON(data);
    console.log(obj);
    var i = 0;
    $.each(obj, function(index, jsonObject){
//      console.log(index);
        console.log(jsonObject) ;
        for (var i=0; i<jsonObject.length; i++){

            contents += "<div class='card'>";
            contents += "<p>Event: <a href='"+ jsonObject[i].get_user_absolute_url +"'>"+jsonObject[i].title+"</a></p>";
            contents += "<p>Location: "+ jsonObject[i].location + "<br>";
            contents += "Date: "+ jsonObject[i].datetime_of_event + "<br>";
            contents += "</div>"
        }

    });
    console.log(contents);
    $('#search-results').html(contents);
}