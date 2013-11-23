import json
from dajaxice.decorators import dajaxice_register
from models import Bondi, Bondi_lists, Bondi_tweet_keywords, Bondi_bio_keywords
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI

@dajaxice_register
def AJ_updateEmail(request,email):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondi.email = email
    bondi.save()
    return json.dumps({'email':email})

@dajaxice_register
def AJ_tweet_keyword(request,keyword_num,tweet_keyword):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0] 
    bondiTweetKeywords = bondiList.bondi_tweet_keywords_set.all()
    bondiTweetKeywords.filter(pk=keyword_num).update(keyword=tweet_keyword)
    return json.dumps({'keyword_num':keyword_num,'tweet_keyword':tweet_keyword})

@dajaxice_register
def AJ_toggleKeywordsRT(request,keywords_RT_flag):
    keywords_RT_flag = not keywords_RT_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_keywords_RT_flag = keywords_RT_flag
    bondiList.save()
    return json.dumps({'keywords_RT_flag':keywords_RT_flag})

@dajaxice_register
def AJ_toggleKeywordsFAV(request,keywords_FAV_flag):
    keywords_FAV_flag = not keywords_FAV_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_keywords_FAV_flag = keywords_FAV_flag
    bondiList.save()
    return json.dumps({'keywords_FAV_flag':keywords_FAV_flag})


RtPopTimeTable = {1:u'10',2:u'20',3:u'30',4:u'60'}
@dajaxice_register
def AJ_updateRtPopTime(request,RtPopTimeChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_popular_time_period = RtPopTimeTable.keys()[RtPopTimeTable.values().index(RtPopTimeChoice)]
    bondiList.save()
    return json.dumps({'RtPopTimeChoice':RtPopTimeChoice})

RtPopMinRTtable = {1:u'1',2:u'2',3:u'3',4:u'5',5:u'10'}
@dajaxice_register
def AJ_updateRtPopMinRT(request,RtPopMinRTChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_popular_RT_threshold = RtPopMinRTtable.keys()[RtPopMinRTtable.values().index(RtPopMinRTChoice)]
    bondiList.save()
    return json.dumps({'RtPopMinRTChoice':RtPopMinRTChoice})
    
RtPopMinFAVtable = {1:u'1',2:u'2',3:u'3',4:u'5',5:u'10'}
@dajaxice_register
def AJ_updateRtPopMinFAV(request,RtPopMinFAVChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_popular_FAV_threshold = RtPopMinFAVtable.keys()[RtPopMinFAVtable.values().index(RtPopMinFAVChoice)]
    bondiList.save()
    return json.dumps({'RtPopMinFAVChoice':RtPopMinFAVChoice})

@dajaxice_register
def AJ_togglePopularRT(request,popular_RT_flag):
    popular_RT_flag = not popular_RT_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_popular_RT_flag = popular_RT_flag
    bondiList.save()
    return json.dumps({'popular_RT_flag':popular_RT_flag})

@dajaxice_register
def AJ_togglePopularFAV(request,popular_FAV_flag):
    popular_FAV_flag = not popular_FAV_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.realtime_popular_FAV_flag = popular_FAV_flag
    bondiList.save()
    return json.dumps({'popular_FAV_flag':popular_FAV_flag})




@dajaxice_register
def AJ_bio_keyword(request,keyword_num,bio_keyword):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0] 
    bondiBioKeywords = bondiList.bondi_bio_keywords_set.all()
    bondiBioKeywords.filter(pk=keyword_num).update(keyword=bio_keyword)
    return json.dumps({'keyword_num':keyword_num,'bio_keyword':bio_keyword})

RepFriendsNumTable = {1:u'2',2:u'5',3:u'10',4:u'30',5:u'50'}
@dajaxice_register
def AJ_updateRepFriendsNum(request,RepFriendsNumChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.report_friends_num = RepFriendsNumTable.keys()[RepFriendsNumTable.values().index(RepFriendsNumChoice)]
    bondiList.save()
    return json.dumps({'RepFriendsNumChoice':RepFriendsNumChoice})

@dajaxice_register
def AJ_updateMeFlag(request,MeFlag):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.report_follows_me_flag = MeFlag
    bondiList.save()
    return json.dumps({'MeFlag':MeFlag})    

@dajaxice_register
def AJ_updateBioFlag(request,BioFlag):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.bondi_lists_set.all()[0]  
    bondiList.report_change_bio_flag = BioFlag
    bondiList.save()
    return json.dumps({'BioFlag':BioFlag})   
    

@dajaxice_register
def AJ_toggleEnabled(request,enabled_flag):
    enabled_flag = not enabled_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0] 
    bondi.active_flag = enabled_flag
    bondi.save()
    return json.dumps({'enabled_flag':enabled_flag})
    
    