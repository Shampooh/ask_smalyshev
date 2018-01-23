$(document).ready(function() {
	//console.log('hello');
	$('.js-vote').on('click', function() {
		var $this = $(this);
		var qid = $this.data('qid');
		var vote = $this.data('vote');
		console.log('qid:' + qid + 'vote:' + vote);
		$.post('/vote/', {
			qid:qid,
			vote:vote,
		}).done(function(data) {
			console.log(data);
		});
		return false;
	})

    $('#logout').on('click', function(event){
        event.preventDefault();
        event.stopPropagation();
        $.post('/logout/', {
        }).done(function(data) {
            console.log(data);
            return false;
        });
        return false;
    })

    $('#new_question').on('click', function(event){
        event.preventDefault();
        event.stopPropagation();
        $.post('', {
            text:$('.new-q-input').val()
        }).done(function(data) {
            console.log(data);
            $('.answer').last().after(data)
            return false;
        });
        return false;
    })

    $('.correct').on('click', function() {
        var $this = $(this);
        var qid = $this.data('qid');
        var aid = $this.data('aid');
        console.log('qid:' + qid + " aid:" + aid);
        $.post('/correct/', {
            qid:qid,
            aid:aid
        }).done(function(data) {
            console.log(data);
        });
        return false;
    })
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
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
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});