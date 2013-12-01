#from django.core.management import setup_environ
import Bondiz.settings
#setup_environ(CrossValidate.settings)
import emailTask
from BondizApp.models import Bondi, List, Tweet_keyword, Bondee, Realtime_log
import time
import BondizApp.useTwitterAPI
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
from django.contrib.auth.models import User
import datetime
import time
from django.utils.timezone import utc
from datetime import datetime
#from BondizApp.ajax import

def runRealtimeTask():
    RtPopTimeTable = {1:u'10',2:u'20',3:u'30',4:u'60'}
    RtPopMinRTtable = {1:u'1',2:u'2',3:u'3',4:u'5',5:u'10'}
    RtPopMinFAVtable = {1:u'1',2:u'2',3:u'3',4:u'5',5:u'10'}    
    for bondi in Bondi.objects.all():
        userID = User.objects.filter(username=bondi.twitter_screen_name)[0].id
        SocialAccountId = SocialAccount.objects.filter(user_id=userID)[0].id 
        APP_KEY = SocialApp.objects.filter(name='Bondiz')[0].client_id 
        APP_SECRET = SocialApp.objects.filter(name='Bondiz')[0].secret
        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
        
        if not bondi.active_flag:
            continue
        
        MINUTES_PARAMETER = 10
        POP_MAX_RT = 0
        POP_MAX_FAV = 0
        KEY_MAX_RT = 0
        KEY_MAX_FAV = 0        
        bondiList = bondi.list_set.all()[0]
        
        count = 200
        trim_user = 0
        exclude_replies = 0
        include_rts = 1
        tweets = BondizApp.useTwitterAPI.ListTimeline(twitter,'Bondiz',bondi.twitter_screen_name,count,trim_user,exclude_replies ,include_rts)
        
        realtime_popular_time_period = int(RtPopTimeTable[bondiList.realtime_popular_time_period])        
        realtime_popular_RT_threshold = int(RtPopMinRTtable[bondiList.realtime_popular_RT_threshold])        
        realtime_popular_FAV_threshold = int(RtPopMinFAVtable[bondiList.realtime_popular_FAV_threshold])

        POP_RTcount = 0
        POP_FAVcount = 0      
        KEY_RTcount = 0
        KEY_FAVcount = 0           
        if len(tweets) > 0:
            for tweet in tweets:
                timeDelta = datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                if (timeDelta.seconds > realtime_popular_time_period * 60) and (timeDelta.seconds > MINUTES_PARAMETER * 60): 
                # tweet is irrelevant by time created  
                    continue
                
                ### POPULAR ###
                elif timeDelta.seconds <= realtime_popular_time_period * 60: 
                # tweet is time relevant for "popular" conditions       
                    if (tweet['retweet_count'] >= realtime_popular_RT_threshold) and (not bondi.realtime_log_set.filter(tweet_id=tweet['id_str'], type="RT")):
                    # RT popular & was not emailed as RT popular before
                        if tweet['retweeted']:
                        # RT done by bondi
                            bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                          type = "RT",
                                                          value = str(tweet['retweet_count']),
                                                          condition = str(realtime_popular_RT_threshold),
                                                          tweet_id = tweet['id_str'],
                                                          tweet_text = tweet['text'],
                                                          RT = 1,
                                                          FAV = 0,
                                                          email_timestamp = "")
                        elif bondiList.realtime_popular_RT_flag and POP_RTcount < POP_MAX_RT:
                        # auto RT is enabled & not overdone
                            BondizApp.useTwitterAPI.ReTweet(twitter,tweet['id_str'])
                            POP_RTcount = POP_RTcount + 1                    
                            bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                          type = "RT",
                                                          value = str(tweet['retweet_count']),
                                                          condition = str(realtime_popular_RT_threshold),
                                                          tweet_id = tweet['id_str'],
                                                          tweet_text = tweet['text'],
                                                          RT = 2,
                                                          FAV = 0,
                                                          email_timestamp = "")   
                        else:
                        # no auto RT will be done - still need to email it
                            bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                          type = "RT",
                                                          value = str(tweet['retweet_count']),
                                                          condition = str(realtime_popular_RT_threshold),
                                                          tweet_id = tweet['id_str'],
                                                          tweet_text = tweet['text'],
                                                          RT = 0,
                                                          FAV = 0,
                                                          email_timestamp = "")                                                                                                      
                    if (tweet['favorite_count'] >= realtime_popular_FAV_threshold) and (not bondi.realtime_log_set.filter(tweet_id=tweet['id_str'], type="FAV")):
                    # FAV popular & was not emailed as RT popular before
                        if tweet['favorited']:
                        # FAV done by bondi
                            bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                          type = "FAV",
                                                          value = str(tweet['favorite_count']),
                                                          condition = str(realtime_popular_FAV_threshold),
                                                          tweet_id = tweet['id_str'],
                                                          tweet_text = tweet['text'],
                                                          RT = 0,
                                                          FAV = 1,
                                                          email_timestamp = "")
                        elif bondiList.realtime_popular_RT_flag and POP_FAVcount < POP_MAX_FAV:
                        # auto FAV is enabled & not overdone
                            BondizApp.useTwitterAPI.Favorite(twitter,tweet['id_str'])
                            POP_FAVcount = POP_FAVcount + 1                    
                            bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                          type = "FAV",
                                                          value = str(tweet['favorite_count']),
                                                          condition = str(realtime_popular_FAV_threshold),
                                                          tweet_id = tweet['id_str'],
                                                          tweet_text = tweet['text'],
                                                          RT = 0,
                                                          FAV = 2,
                                                          email_timestamp = "")                     
                        else:
                        # no auto FAV will be done - still need to email it
                            bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                          type = "FAV",
                                                          value = str(tweet['favorite_count']),
                                                          condition = str(realtime_popular_FAV_threshold),
                                                          tweet_id = tweet['id_str'],
                                                          tweet_text = tweet['text'],
                                                          RT = 0,
                                                          FAV = 0,
                                                          email_timestamp = "")                            
                            
                            
                ### KEYWORDS ###                                                                  
                elif timeDelta.seconds <= MINUTES_PARAMETER * 60:
                # tweet is time relevant for "keyword" conditions  
                    keyword_list = [x['keyword'] for x in bondiList.tweet_keyword_set.all().values()]
                    
                    if any(keyword in tweet['text'] for keyword in filter(None,keyword_list)): 
                    # tweet has keywords inside
                    
                        # RT #
                        if tweet['retweeted']:
                        # RT done by bondi
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword in tweet['text']:
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  type = "KEY",
                                                                  value = "",
                                                                  condition = keyword,
                                                                  tweet_id = tweet['id_str'],
                                                                  tweet_text = tweet['text'],
                                                                  RT = 1,
                                                                  FAV = 0,
                                                                  email_timestamp = "")
                        if bondiList.realtime_keywords_RT_flag and KEY_RTcount < KEY_MAX_RT:                                    
                        # auto RT is enabled & not overdone
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword in tweet['text']:
                                    BondizApp.useTwitterAPI.ReTweet(twitter,tweet['id_str'])
                                    KEY_RTcount = KEY_RTcount + 1 
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                      type = "KEY",
                                                                      value = "",
                                                                      condition = keyword,
                                                                      tweet_id = tweet['id_str'],
                                                                      tweet_text = tweet['text'],
                                                                      RT = 2,
                                                                      FAV = 0,
                                                                      email_timestamp = "")  
                        else:
                        # no auto RT will be done - still need to email it 
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword in tweet['text']:
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                      type = "KEY",
                                                                      value = "",
                                                                      condition = keyword,
                                                                      tweet_id = tweet['id_str'],
                                                                      tweet_text = tweet['text'],
                                                                      RT = 0,
                                                                      FAV = 0,
                                                                      email_timestamp = "")    

                        # FAV #
                        if tweet['favorited']:
                        # FAV done by bondi
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword in tweet['text']:
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  type = "KEY",
                                                                  value = "",
                                                                  condition = keyword,
                                                                  tweet_id = tweet['id_str'],
                                                                  tweet_text = tweet['text'],
                                                                  RT = 0,
                                                                  FAV = 1,
                                                                  email_timestamp = "")
                        if bondiList.realtime_keywords_FAV_flag and KEY_FAVcount < KEY_MAX_FAV:                                    
                        # auto FAV is enabled & not overdone
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword in tweet['text']:
                                    BondizApp.useTwitterAPI.ReTweet(twitter,tweet['id_str'])
                                    KEY_FAVcount = KEY_FAVcount + 1 
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                      type = "KEY",
                                                                      value = "",
                                                                      condition = keyword,
                                                                      tweet_id = tweet['id_str'],
                                                                      tweet_text = tweet['text'],
                                                                      RT = 0,
                                                                      FAV = 2,
                                                                      email_timestamp = "")  
                        else:
                        # no auto FAV will be done - still need to email it 
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword in tweet['text']:
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                      type = "KEY",
                                                                      value = "",
                                                                      condition = keyword,
                                                                      tweet_id = tweet['id_str'],
                                                                      tweet_text = tweet['text'],
                                                                      RT = 0,
                                                                      FAV = 0,
                                                                      email_timestamp = "")                                                                                           
                    
                        
        emailTask.runEmailTask()
    return 1

if __name__=='__main__':
    tic = time.clock()
    runRealtimeTask() 
    toc = time.clock()
    print ['RealtimeTask done in '+ str(toc) + ' seconds']