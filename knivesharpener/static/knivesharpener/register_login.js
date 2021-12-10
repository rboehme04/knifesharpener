$(function() {

    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
        $('#bottom_line').removeClass('bottom_line_register');
        $('#bottom_line').addClass('bottom_line_login');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
        $('#bottom_line').removeClass('bottom_line_login');
        $('#bottom_line').addClass('bottom_line_register');
		e.preventDefault();
       
	});
});