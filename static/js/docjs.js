function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	// $(".g-signin2").css("display", "none");
	// $(".data").css("display", "block");
	$("#pic").attr('src',profile.getImageUrl());
	$("#email").text(profile.getEmail());

	// window.location = "/persondoc";

	// var getemail = document.getElementById("email").value;

      //       $.ajax({
      //           url: '/persondoc',
      //           data: JSON.stringify({"getemail" : getemail}),
      //           type: 'POST',
      //           processData: false,
      //           contentType: 'application/json; charset=utf-8',
      //           success: function(response){
      //               console.log(response);
      //           },
      //           error: function(error){
      //               console.log(error);
      //           }
      //       });
}

function signOut(){
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function(){
		alert("You have been successfully signed out");
		// $(".g-signin2").css("display","block");
		// $(".data").css("display","none");
		window.location = "/signinpersondoc";
	});
}