$(document).ready(function(){
	$(".tab").click(function(){
		var x = $(this).attr("id");
		if(x == "signup"){
			$("#signin").removeClass("select");
			$("#signup").addClass("select");
			$("#signupbox").slideDown();
			$("#signinbox").slideUp();
		}
		else{
			$("#signup").removeClass("select");
			$("#signin").addClass("select");
			$("#signinbox").slideDown();
			$("#signupbox").slideUp();
		}
	});
});