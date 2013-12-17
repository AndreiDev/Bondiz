$(document).ready(function () {	
	
	$("[data-toggle='tooltip']").tooltip({'placement': 'bottom'});
		
	isUsernameValid = false;
	isEmailValid = false;

	function isInputsValid(){
		return (isUsernameValid && isEmailValid);
	}
	
	function IsAlphaNumeric(text) {
  		var regex = /^[a-zA-Z0-9_]{1,15}$/;
  		return regex.test(text);
	}	
	
	function IsEmail(email) {
  		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  		return regex.test(email);
	}	
	
	$('#username').change(function() { 
		if (IsAlphaNumeric($('#username').val())){
			$('#username').removeClass('bad-input');
			isUsernameValid = true;				
		}
		else {
			isUsernameValid = false;
			$('#username').addClass('bad-input');
		}			
	})
	
	
	$('#email').change(function() { 
		if (IsEmail($('#email').val())){
			$('#email').removeClass('bad-input');
			isEmailValid = true;				
		}
		else {
			isEmailValid = false;
			$('#email').addClass('bad-input');
		}			
	})

	function goCallback(data){		
		if (data.res == '91'){
			$('#91Modal').modal('show')
			isUsernameValid = false;
			$('#username').addClass('bad-input');	
		}
		else if (data.res == '92') {
			isUsernameValid = false;
			$('#username').addClass('bad-input');			
			$('#92Modal').modal('show')
		}
		else if (data.res == '93') {
			isEmailValid = false;
			$('#email').addClass('bad-input');	
			$('#93Modal').modal('show')
		}		
		else {
			$('#username').val("");	
			isUsernameValid = false;
			$('#email').val("");
			isEmailValid = false;			
			$('#OKModal').modal('show')
		}
		$('#go').removeAttr('disabled');
	}	

	$('#go').click(function() {
		if (isInputsValid()){
			$('#go').attr('disabled','disabled');
			Dajaxice.BondizApp.AJ_go(goCallback,{
				'username':$('#username').val(),
				'email':$('#email').val(),
				});	
		} else {

			if (IsAlphaNumeric($('#username').val())){
				$('#username').removeClass('bad-input');
				isUsernameValid = true;				
			}
			else {
				isUsernameValid = false;
				$('#username').addClass('bad-input');
			}	
		
			if (IsEmail($('#email').val())){
				$('#email').removeClass('bad-input');
				isEmailValid = true;				
			}
			else {
				isEmailValid = false;
				$('#email').addClass('bad-input');
			}	
			if (isInputsValid()){
				$('#go').attr('disabled','disabled');
				Dajaxice.BondizApp.AJ_go(goCallback,{
					'username':$('#username').val(),
					'email':$('#email').val(),
					});
			}									
		} 
	})	
});