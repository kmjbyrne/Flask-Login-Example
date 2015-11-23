
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

        $.ajax({
            url: '/register',
            data: $('#form').serialize(),
            type: 'POST',
            success: function(data)
            {
                if (data.status == 'OK')
                { 
                    $('.modal.in').modal('hide') 
                    $('.description').html("<h1>Please use your new login details to continue!<h1>");
                }
                else if (data.status == 'EXIST')
                { 
                    alert_exists();
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
});

function login_redirect(){
    window.location ='/home';
}

function alert_exists(){
    alert("Username (email) already exists, please enter a different email");
}