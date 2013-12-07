import json
from dajaxice.decorators import dajaxice_register
from models import Bondi, List, Tweet_keyword, Bondee, Realtime_log, Daily_log
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI

@dajaxice_register
def AJ_UpdateAll(request,email,tweet_keyword1,tweet_keyword2,tweet_keyword3,tweet_keyword4,tweet_keyword5,
                 keywords_RT_flag,keywords_FAV_flag,RtPopTimeChoice,RtPopMinRTChoice,RtPopMinFAVChoice,popular_RT_flag,
                 popular_FAV_flag,RepFollowersNumChoice,RepFriendsNumChoice,MeFlag,BioFlag,enabled_flag):
    email = updateEmail(request,email)
    tweet_keyword1 = tweet_keyword(request,1,tweet_keyword1)
    tweet_keyword2 = tweet_keyword(request,2,tweet_keyword2)
    tweet_keyword3 = tweet_keyword(request,3,tweet_keyword3)
    tweet_keyword4 = tweet_keyword(request,4,tweet_keyword4)
    tweet_keyword5 = tweet_keyword(request,5,tweet_keyword5)
    keywords_RT_flag = toggleKeywordsRT(request,keywords_RT_flag)
    keywords_FAV_flag = toggleKeywordsFAV(request,keywords_FAV_flag)
    RtPopTimeChoice = updateRtPopTime(request,RtPopTimeChoice)
    RtPopMinRTChoice = updateRtPopMinRT(request,RtPopMinRTChoice)
    RtPopMinFAVChoice = updateRtPopMinFAV(request,RtPopMinFAVChoice)
    popular_RT_flag = togglePopularRT(request,popular_RT_flag)
    popular_FAV_flag = togglePopularFAV(request,popular_FAV_flag)
    RepFollowersNumChoice = updateRepFollowersNum(request,RepFollowersNumChoice)
    RepFriendsNumChoice = updateRepFriendsNum(request,RepFriendsNumChoice)
    MeFlag = updateMeFlag(request,MeFlag)
    BioFlag = updateBioFlag(request,BioFlag)
    enabled_flag = toggleEnabled(request,enabled_flag)
    return json.dumps({'email':email,'tweet_keyword1':tweet_keyword1,'tweet_keyword2':tweet_keyword2,'tweet_keyword3':tweet_keyword3,'tweet_keyword4':tweet_keyword4,'tweet_keyword5':tweet_keyword5,
                       'keywords_RT_flag':keywords_RT_flag,'keywords_FAV_flag':keywords_FAV_flag,'RtPopTimeChoice':RtPopTimeChoice,'RtPopMinRTChoice':RtPopMinRTChoice,
                       'RtPopMinFAVChoice':RtPopMinFAVChoice,'popular_RT_flag':popular_RT_flag,'popular_FAV_flag':popular_FAV_flag,'RepFollowersNumChoice':RepFollowersNumChoice,
                       'RepFriendsNumChoice':RepFriendsNumChoice,'MeFlag':MeFlag,'BioFlag':BioFlag,'enabled_flag':enabled_flag})

def updateEmail(request,email):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondi.email = email
    bondi.save()
    return bondi.email

def tweet_keyword(request,keyword_num,tweet_keyword):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0] 
    bondiTweetKeyword = bondiList.tweet_keyword_set.filter(place=keyword_num)[0]
    bondiTweetKeyword.keyword = tweet_keyword
    bondiTweetKeyword.save()
    return bondiTweetKeyword.keyword

def toggleKeywordsRT(request,keywords_RT_flag):
    keywords_RT_flag = not keywords_RT_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_keywords_RT_flag = keywords_RT_flag
    bondiList.save()
    return bondiList.realtime_keywords_RT_flag

def toggleKeywordsFAV(request,keywords_FAV_flag):
    keywords_FAV_flag = not keywords_FAV_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_keywords_FAV_flag = keywords_FAV_flag
    bondiList.save()
    return bondiList.realtime_keywords_FAV_flag

def updateRtPopTime(request,RtPopTimeChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_popular_time_period = RtPopTimeChoice
    bondiList.save()
    return bondiList.realtime_popular_time_period

def updateRtPopMinRT(request,RtPopMinRTChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_popular_RT_threshold = RtPopMinRTChoice
    bondiList.save()
    return bondiList.realtime_popular_RT_threshold
    
def updateRtPopMinFAV(request,RtPopMinFAVChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_popular_FAV_threshold = RtPopMinFAVChoice
    bondiList.save()
    return bondiList.realtime_popular_FAV_threshold

def togglePopularRT(request,popular_RT_flag):
    popular_RT_flag = not popular_RT_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_popular_RT_flag = popular_RT_flag
    bondiList.save()
    return bondiList.realtime_popular_RT_flag

def togglePopularFAV(request,popular_FAV_flag):
    popular_FAV_flag = not popular_FAV_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.realtime_popular_FAV_flag = popular_FAV_flag
    bondiList.save()
    return bondiList.realtime_popular_FAV_flag

def updateRepFollowersNum(request,RepFollowersNumChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.report_followers_num = RepFollowersNumChoice
    bondiList.save()
    return bondiList.report_followers_num

def updateRepFriendsNum(request,RepFriendsNumChoice):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.report_friends_num = RepFriendsNumChoice
    bondiList.save()
    return bondiList.report_friends_num

def updateMeFlag(request,MeFlag):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.report_follows_me_flag = MeFlag
    bondiList.save()
    return bondiList.report_follows_me_flag

def updateBioFlag(request,BioFlag):
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
    bondiList = bondi.list_set.all()[0]  
    bondiList.report_change_bio_flag = BioFlag
    bondiList.save()
    return bondiList.report_change_bio_flag
    
def toggleEnabled(request,enabled_flag):
    enabled_flag = not enabled_flag # toggling the flag
    bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0] 
    bondiList = bondi.list_set.all()[0]  
    bondiList.active_flag = enabled_flag
    bondiList.save()
    return bondiList.active_flag
