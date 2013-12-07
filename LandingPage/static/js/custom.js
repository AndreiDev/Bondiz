$(document).ready(function () {	
	$("[data-toggle='tooltip']").tooltip({'placement': 'top'});
	
	
	// SETTINGS page
	
	isEmailValid = true;
	isKey1Valid = true;
	isKey2Valid = true;
	isKey3Valid = true;
	isKey4Valid = true;
	isKey5Valid = true;
	
	function isInputsValid(){
		return (isEmailValid && isKey1Valid && isKey2Valid && isKey3Valid && isKey4Valid && isKey5Valid);
	}
	
	$('#saveChanges').attr('disabled','disabled');
	
	function IsAlphaNumeric(text) {
  		var regex = /^[a-zA-Z0-9_]+$/;
  		return regex.test(text);
	}	
	
	function IsEmail(email) {
  		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  		return regex.test(email);
	}	
	
	$('#email').change(function() { 
		if ((IsEmail($('#email').val())) || ($('#email').val() == "")){
			$('#email').removeClass('bad-input');
			isEmailValid = true;
			if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}						
		}
		else {
			isEmailValid = false;
			$('#saveChanges').attr('disabled','disabled');
			$('#email').addClass('bad-input');
		}			
	})

	$('#tweet_keyword1').change(function() { 	
		if (($('#tweet_keyword1').val() == "") || (IsAlphaNumeric($('#tweet_keyword1').val()))){
			$('#tweet_keyword1').removeClass('bad-input');
			isKey1Valid = true;
			if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}					
		}
		else {
			isKey1Valid = false;
			$('#saveChanges').attr('disabled','disabled');
			$('#tweet_keyword1').addClass('bad-input');
		}		
	})
	$('#tweet_keyword2').change(function() { 	
		if (($('#tweet_keyword2').val() == "") || (IsAlphaNumeric($('#tweet_keyword2').val()))){
			$('#tweet_keyword2').removeClass('bad-input');
			isKey2Valid = true;
			if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}							
		}
		else {
			isKey2Valid = false;
			$('#saveChanges').attr('disabled','disabled');
			$('#tweet_keyword2').addClass('bad-input');
		}		
	})
	$('#tweet_keyword3').change(function() { 	
		if (($('#tweet_keyword3').val() == "") || (IsAlphaNumeric($('#tweet_keyword3').val()))){
			$('#tweet_keyword3').removeClass('bad-input');
			isKey3Valid = true;
			if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}							
		}
		else {
			isKey3Valid = false;
			$('#saveChanges').attr('disabled','disabled');
			$('#tweet_keyword3').addClass('bad-input');
		}		
	})
	$('#tweet_keyword4').change(function() { 	
		if (($('#tweet_keyword4').val() == "") || (IsAlphaNumeric($('#tweet_keyword4').val()))){
			$('#tweet_keyword4').removeClass('bad-input');
			isKey4Valid = true;
			if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}						
		}
		else {
			isKey4Valid = false;
			$('#saveChanges').attr('disabled','disabled');
			$('#tweet_keyword4').addClass('bad-input');
		}		
	})
	$('#tweet_keyword5').change(function() { 	
		if (($('#tweet_keyword5').val() == "") || (IsAlphaNumeric($('#tweet_keyword5').val()))){
			$('#tweet_keyword5').removeClass('bad-input');
			isKey5Valid = true;
			if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}						
		}
		else {
			isKey5Valid = false;
			$('#saveChanges').attr('disabled','disabled');
			$('#tweet_keyword5').addClass('bad-input');
		}		
	})

	$('#keywordsRT').click(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}					
	})	
	
	$('#keywordsFAV').click(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}		
	})		

	$('#rt_pop_time').change(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}	
	})	

	$('#rt_pop_RT').change(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}	
	})
	
	$('#rt_pop_FAV').change(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}		
	})		

	$('#popularRT').click(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}		
	})	
		
	$('#popularFAV').click(function() {
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}		
	})	
	
	$('#rep_followers_num').change(function() {
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}	
	})			

	$('#rep_friends_num').change(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}	
	})	

	$('#meFlag').change(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}	
	})		

	$('#bioFlag').change(function() { 
		if (isInputsValid()){$('#saveChanges').removeAttr('disabled');}	
	})					

	$('#enabledFlag').click(function() { 
		if (!$('#enabledFlag').hasClass('active')){
			$('#enabledFlag').text('Account active');
		} else {
			$('#enabledFlag').text('Account inactive');
		}			
		if (isInputsValid()){
			$('#saveChanges').removeAttr('disabled');
		}	
	})	

	function updateAllCallback(data){		
		$('#email').val(data.email);	
		$('#tweet_keyword1').val(data.tweet_keyword1);
		$('#tweet_keyword2').val(data.tweet_keyword2);
		$('#tweet_keyword3').val(data.tweet_keyword3);
		$('#tweet_keyword4').val(data.tweet_keyword4);
		$('#tweet_keyword5').val(data.tweet_keyword5);	
		if (data.keywords_RT_flag){
			$('#keywordsRT').addClass('active');
		} else {
			$('#keywordsRT').removeClass('active');
		}
		if (data.keywords_FAV_flag){
			$('#keywordsFAV').addClass('active');
		} else {
			$('#keywordsFAV').removeClass('active');
		}
		$('#rt_pop_time').val(data.RtPopTimeChoice);
		$('#rt_pop_RT').val(data.RtPopMinRTChoice);
		$('#rt_pop_FAV').val(data.RtPopMinFAVChoice);
		if (data.popular_RT_flag){
			$('#popularRT').addClass('active');
		} else {
			$('#popularRT').removeClass('active');
		}
		if (data.popular_FAV_flag){
			$('#popularFAV').addClass('active');
		} else {
			$('#popularFAV').removeClass('active');
		}
		$('#rep_followers_num').val(data.RepFollowersNumChoice);
		$('#rep_friends_num').val(data.RepFriendsNumChoice);
		$('#meFlag').attr("checked",data.MeFlag);
		$('#bioFlag').attr("checked",data.BioFlag);
		if (data.enabled_flag){
			$('#enabledFlag').addClass('active');
			$('#enabledFlag').text('Account active');
		} else {
			$('#enabledFlag').removeClass('active');
			$('#enabledFlag').text('Account inactive');
		}		
	}	

	$('#saveChanges').click(function() {
		if (isInputsValid()){
			$('#saveChanges').attr('disabled','disabled');
			Dajaxice.BondizApp.AJ_UpdateAll(updateAllCallback,{
				'email':$('#email').val(),
				'tweet_keyword1':$('#tweet_keyword1').val(),
				'tweet_keyword2':$('#tweet_keyword2').val(),
				'tweet_keyword3':$('#tweet_keyword3').val(),
				'tweet_keyword4':$('#tweet_keyword4').val(),
				'tweet_keyword5':$('#tweet_keyword5').val(),
				'keywords_RT_flag':!$('#keywordsRT').hasClass('active'),
				'keywords_FAV_flag':!$('#keywordsFAV').hasClass('active'),
				'RtPopTimeChoice':$('#rt_pop_time').val(),
				'RtPopMinRTChoice':$('#rt_pop_RT').val(),
				'RtPopMinFAVChoice':$('#rt_pop_FAV').val(),
				'popular_RT_flag':!$('#popularRT').hasClass('active'),
				'popular_FAV_flag':!$('#popularFAV').hasClass('active'),
				'RepFollowersNumChoice':$('#rep_followers_num').val(),
				'RepFriendsNumChoice':$('#rep_friends_num').val(),
				'MeFlag':$('#meFlag').is(':checked'),
				'BioFlag':$('#bioFlag').is(':checked'),
				'enabled_flag':!$('#enabledFlag').hasClass('active')
				});	
		} else {
			$('#saveChanges').attr('disabled','disabled');
		} 
	})
		//Dajaxice.BondizApp.AJ_updateEmail(updatedEmail,{'email':$('#email').val()});		
		//Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':1,'tweet_keyword':$('#tweet_keyword1').val()});			
		//Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':2,'tweet_keyword':$('#tweet_keyword2').val()});	
		//Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':3,'tweet_keyword':$('#tweet_keyword3').val()});	
		//Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':4,'tweet_keyword':$('#tweet_keyword4').val()});	
		//Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':5,'tweet_keyword':$('#tweet_keyword5').val()});	
		//Dajaxice.BondizApp.AJ_toggleKeywordsRT(toggledKeywordsRT,{'keywords_RT_flag':$('#keywordsRT').hasClass('active')});
		//Dajaxice.BondizApp.AJ_toggleKeywordsFAV(toggledKeywordsFAV,{'keywords_FAV_flag':$('#keywordsFAV').hasClass('active')});
		//Dajaxice.BondizApp.AJ_updateRtPopTime(updatedRtPopTime,{'RtPopTimeChoice':$('#rt_pop_time').val()});			
		//Dajaxice.BondizApp.AJ_updateRtPopMinRT(updatedRtPopMinRT,{'RtPopMinRTChoice':$('#rt_pop_RT').val()});			
		//Dajaxice.BondizApp.AJ_updateRtPopMinFAV(updatedRtPopMinFAV,{'RtPopMinFAVChoice':$('#rt_pop_FAV').val()});		
		//Dajaxice.BondizApp.AJ_togglePopularRT(toggledPopularRT,{'popular_RT_flag':$('#popularRT').hasClass('active')});		
		//Dajaxice.BondizApp.AJ_togglePopularFAV(toggledPopularFAV,{'popular_FAV_flag':$('#popularFAV').hasClass('active')});		
		//Dajaxice.BondizApp.AJ_updateRepFollowersNum(updatedRepFollowersNum,{'RepFollowersNumChoice':$('#rep_followers_num').val()});		
		//Dajaxice.BondizApp.AJ_updateRepFriendsNum(updatedRepFriendsNum,{'RepFriendsNumChoice':$('#rep_friends_num').val()});		
		//Dajaxice.BondizApp.AJ_updateMeFlag(updatedMeFlag,{'MeFlag':$('#meFlag').is(':checked')});			
		//Dajaxice.BondizApp.AJ_updateBioFlag(updatedBioFlag,{'BioFlag':$('#bioFlag').is(':checked')});			
		//Dajaxice.BondizApp.AJ_toggleEnabled(toggledEnabled,{'enabled_flag':$('#enabledFlag').hasClass('active')});		
});