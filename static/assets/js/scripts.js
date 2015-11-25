/*

Author: Keith Byrne
Date: 16/11/2015

JS and AJAX below. See corresponding PY code for JSON return
*/

$(document).ready(function(){
    /*
        Fullscreen background
    */
    $.backstretch("assets/img/backgrounds/1.jpg");
    /*
	    Modals
	*/
	$('.launch-modal').on('click', function(e){
		e.preventDefault();
		$( '#' + $(this).data('modal-id') ).modal();
	});

    /*
        Form validation
    */
    $('.registration-form input[type="text"], .registration-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });

    //Ajax js for submitting login request
    $('.registration-form').on('submit', function(e) {
    	$(this).find('input[type="text"], textarea').each(function(){
    		if( $(this).val() == "" )
            {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});

        $('#loading-anim').empty().append('<div class="spinner-loader">Processing.... </div>');
        $.ajax({
            url: '/register',
            data: $('#form').serialize(),
            type: 'POST',
            success: function(data)
            {
                if (data.status == 'OK')
                {
                    $('.modal.in').modal('hide')
                    $('.description').html("<h1>Registration successful, please await your verification mail!<h1>");
                    $('.loading-anim').empty();
                }
                else if (data.status == 'EXIST')
                {
                    alert_exists();
                    $('#loading-anim').empty().append('<button type="submit" class="btn">Sign me up!</button>');
                }
                else
                {

                }
            }
        });
        // -- End AJAX Call --
        return false;
    });

    //Ajax js for submitting login request
    $('.login-form').on('submit', function(e) {
        $(this).find('input[type="text"], textarea').each(function(){
            if( $(this).val() == "" )
            {
                e.preventDefault();
                $(this).addClass('input-error');
            }
            else {
                $(this).removeClass('input-error');
            }
        });

        $.ajax({
            url: '/login',
            data: $('.login-form').serialize(),
            type: 'POST',
            success: function(data)
            {
                if (data.status == 'OK')
                {
                    login_redirect();
                }
                else if (data.status == 'NON_VERIFIED')
                {
                    $('.modal-title').html("It appears you haven't verified your email. Please do so to login!");
                }
                else if (data.status == 'NONE')
                {
                    $('.modal-title').html("Username entered does not exist!");
                }
                else if (data.status == 'WRONG')
                {
                    $('.modal-title').html("Invalid details, try again!");
                }
            }
        });
        // -- End AJAX Call --
        return false;
    });

    $('#question').click(function(){
        alert("The number 42 is!");
    });
});

function login_redirect(){
    window.location ='/home';
}

function alert_exists(){
    alert("Username (email) already exists, please enter a different email");
}