$(document).ready(function() {

    // AJAX GET
    $('#get-more').click(function(){
        console.log('Get is called');
        
        $.ajax({
            type: "GET",
            url: "/jav/more",
            success: function(data) {
                for(i = 0; i < data.length; i++){
                    $('ul').append('<li>'+data[i]+'</li>');
                }
            }
        });

    });


    // AJAX POST
    $('#add-todo').click(function(){
        console.log('am i called' + $("#item").val());

        $.ajax({
            type: "POST",
            url: "/jav/add_todo",
            dataType: "json",
            data: { "item": $("#item").val() },
            success: function(data) {
                alert(data.message);
            }
        });

    });
    
    $('.likes').click(function(){
        
        var act_id = $(this).attr('data-catid');
        
        //console.log("likes is called " + act_id);

        $.ajax({
            type: "GET",
            url: "/jav/like_actress",
            dataType: "json",
            data: {"actress_id": act_id},
            success: function(data) {
                console.log("Success" + data);
                $('.like_count[data-catid=' + act_id +']').html("Like " + data);
                // $('.likes').hide()
            }
        });

    });



    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 


});