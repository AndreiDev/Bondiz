$(document).ready(function () {	
	$("[data-toggle='tooltip']").tooltip({'placement': 'top'});
	
	
	function IsAlphaNumeric(text) {
  		var regex = /^[a-zA-Z0-9_]+$/;
  		return regex.test(text);
	}	
	
	function IsEmail(email) {
  		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  		return regex.test(email);
	}	
	
	$('#alert_email').hide();
	$('#alert_tweet_keyword1').hide();	
	$('#alert_tweet_keyword2').hide();
	$('#alert_tweet_keyword3').hide();	
	$('#alert_tweet_keyword4').hide();
	$('#alert_tweet_keyword5').hide();
	$('#alert_bio_keyword1').hide();	
	$('#alert_bio_keyword2').hide();
	$('#alert_bio_keyword3').hide();	
	$('#alert_bio_keyword4').hide();
	$('#alert_bio_keyword5').hide();
	
	function updatedEmail(data){
		$('#email').val(data.email);	
	}
	$('#email').change(function() { 
		$('#alert_email').hide();	
		if ($('#email').val() != ""){
			if (IsEmail($('#email').val())){
				Dajaxice.BondizApp.AJ_updateEmail(updatedEmail,{'email':$('#email').val()});			
			}
			else {
				$('#alert_email').show();
			}
		}			
	})

	function updated_tweet_keyword(data){
		$('#tweet_keyword'+data.keyword_num).val(data.tweet_keyword);	
	}
	$('#tweet_keyword1').change(function() { 
		$('#alert_tweet_keyword1').hide();	
		if (($('#tweet_keyword1').val() == "") || (IsAlphaNumeric($('#tweet_keyword1').val()))){
			Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':1,'tweet_keyword':$('#tweet_keyword1').val()});			
		}
		else {
			$('#alert_tweet_keyword1').show();
		}		
	})
	$('#tweet_keyword2').change(function() { 
		$('#alert_tweet_keyword2').hide();	
		if (($('#tweet_keyword2').val() == "") || (IsAlphaNumeric($('#tweet_keyword2').val()))){
			Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':2,'tweet_keyword':$('#tweet_keyword2').val()});			
		}
		else {
			$('#alert_tweet_keyword2').show();
		}		
	})	
	$('#tweet_keyword3').change(function() { 
		$('#alert_tweet_keyword3').hide();	
		if (($('#tweet_keyword3').val() == "") || (IsAlphaNumeric($('#tweet_keyword3').val()))){
			Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':3,'tweet_keyword':$('#tweet_keyword3').val()});			
		}
		else {
			$('#alert_tweet_keyword3').show();
		}		
	})
	$('#tweet_keyword4').change(function() { 
		$('#alert_tweet_keyword4').hide();	
		if (($('#tweet_keyword4').val() == "") || (IsAlphaNumeric($('#tweet_keyword4').val()))){
			Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':4,'tweet_keyword':$('#tweet_keyword4').val()});			
		}
		else {
			$('#alert_tweet_keyword4').show();
		}		
	})
	$('#tweet_keyword5').change(function() { 
		$('#alert_tweet_keyword5').hide();	
		if (($('#tweet_keyword5').val() == "") || (IsAlphaNumeric($('#tweet_keyword5').val()))){
			Dajaxice.BondizApp.AJ_tweet_keyword(updated_tweet_keyword,{'keyword_num':5,'tweet_keyword':$('#tweet_keyword5').val()});			
		}
		else {
			$('#alert_tweet_keyword5').show();
		}		
	})

	function toggledKeywordsRT(data){
		if (data.keywords_RT_flag){
			$('#keywordsRT').addClass('active');
			$('#keywordsRT').text('Auto Retweet on');
		} else {
			$('#keywordsRT').removeClass('active');
			$('#keywordsRT').text('Auto Retweet off');
		}
	}	
	$('#keywordsRT').click(function() { 
		Dajaxice.BondizApp.AJ_toggleKeywordsRT(toggledKeywordsRT,{'keywords_RT_flag':$('#keywordsRT').hasClass('active')});	
	})	
	
	function toggledKeywordsFAV(data){
		if (data.keywords_FAV_flag){
			$('#keywordsFAV').addClass('active');
			$('#keywordsFAV').text('Auto Favorite on');
		} else {
			$('#keywordsFAV').removeClass('active');
			$('#keywordsFAV').text('Auto Favorite off');
		}
	}	
	$('#keywordsFAV').click(function() { 
		Dajaxice.BondizApp.AJ_toggleKeywordsFAV(toggledKeywordsFAV,{'keywords_FAV_flag':$('#keywordsFAV').hasClass('active')});	
	})		


	function updatedRtPopTime(data){
		$('#rt_pop_time').val(data.RtPopTimeChoice);
	}
	$('#rt_pop_time').change(function() { 
		Dajaxice.BondizApp.AJ_updateRtPopTime(updatedRtPopTime,{'RtPopTimeChoice':$('#rt_pop_time').val()});	
	})	
	
	function updatedRtPopMinRT(data){
		$('#rt_pop_RT').val(data.RtPopMinRTChoice);
	}
	$('#rt_pop_RT').change(function() { 
		Dajaxice.BondizApp.AJ_updateRtPopMinRT(updatedRtPopMinRT,{'RtPopMinRTChoice':$('#rt_pop_RT').val()});	
	})
	
	function updatedRtPopMinFAV(data){
		$('#rt_pop_FAV').val(data.RtPopMinFAVChoice);
	}
	$('#rt_pop_FAV').change(function() { 
		Dajaxice.BondizApp.AJ_updateRtPopMinFAV(updatedRtPopMinFAV,{'RtPopMinFAVChoice':$('#rt_pop_FAV').val()});	
	})		

	function toggledPopularRT(data){
		if (data.popular_RT_flag){
			$('#popularRT').addClass('active');
			$('#popularRT').text('Auto Retweet on');
		} else {
			$('#popularRT').removeClass('active');
			$('#popularRT').text('Auto Retweet off');
		}
	}	
	$('#popularRT').click(function() { 
		Dajaxice.BondizApp.AJ_togglePopularRT(toggledPopularRT,{'popular_RT_flag':$('#popularRT').hasClass('active')});	
	})	
	
	function toggledPopularFAV(data){
		if (data.popular_FAV_flag){
			$('#popularFAV').addClass('active');
			$('#popularFAV').text('Auto Favorite on');
		} else {
			$('#popularFAV').removeClass('active');
			$('#popularFAV').text('Auto Favorite off');
		}
	}	
	$('#popularFAV').click(function() { 
		Dajaxice.BondizApp.AJ_togglePopularFAV(toggledPopularFAV,{'popular_FAV_flag':$('#popularFAV').hasClass('active')});	
	})	


		
		
	function updatedRepFollowersNum(data){
		$('#rep_followers_num').val(data.RepFollowersNumChoice);
	}
	$('#rep_followers_num').change(function() { 
		Dajaxice.BondizApp.AJ_updateRepFollowersNum(updatedRepFollowersNum,{'RepFollowersNumChoice':$('#rep_followers_num').val()});	
	})			
	
	function updatedRepFriendsNum(data){
		$('#rep_friends_num').val(data.RepFriendsNumChoice);
	}
	$('#rep_friends_num').change(function() { 
		Dajaxice.BondizApp.AJ_updateRepFriendsNum(updatedRepFriendsNum,{'RepFriendsNumChoice':$('#rep_friends_num').val()});	
	})	

	function updatedMeFlag(data){
		$('#meFlag').attr("checked",data.MeFlag);
	}
	$('#meFlag').change(function() { 
		Dajaxice.BondizApp.AJ_updateMeFlag(updatedMeFlag,{'MeFlag':$('#meFlag').is(':checked')});	
	})		

	function updatedBioFlag(data){
		$('#bioFlag').attr("checked",data.BioFlag);
	}
	$('#bioFlag').change(function() { 
		Dajaxice.BondizApp.AJ_updateBioFlag(updatedBioFlag,{'BioFlag':$('#bioFlag').is(':checked')});	
	})					
		
	function toggledEnabled(data){
		if (data.enabled_flag){
			$('#enabledFlag').addClass('active');
			$('#enabledFlag').text('Account is active');
		} else {
			$('#enabledFlag').removeClass('active');
			$('#enabledFlag').text('Account is inactive');
		}
	}	
	$('#enabledFlag').click(function() { 
		Dajaxice.BondizApp.AJ_toggleEnabled(toggledEnabled,{'enabled_flag':$('#enabledFlag').hasClass('active')});	
	})		
});