#from django.core.management import setup_environ
import Bondiz.settings
#setup_environ(CrossValidate.settings)
import emailTask
from BondizApp.models import Bondi, List, Tweet_keyword, Bondee, Realtime_log
import time
from debug import debug
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
    debug('RealtimeTask started')
    RtPopTimeTable = {1:u'10',2:u'20',3:u'30',4:u'60'}
    RtPopMinRTtable = {1:u'1',2:u'2',3:u'3',4:u'5',5:u'10'}
    RtPopMinFAVtable = {1:u'1',2:u'2',3:u'3',4:u'5',5:u'10'}    
    for bondi in Bondi.objects.all():
        debug('processing bondi ' + bondi.twitter_screen_name)
        
        userID = User.objects.filter(username=bondi.twitter_screen_name)[0].id
        SocialAccountId = SocialAccount.objects.filter(user_id=userID)[0].id 
        APP_KEY = SocialApp.objects.filter(name='Bondiz')[0].client_id 
        APP_SECRET = SocialApp.objects.filter(name='Bondiz')[0].secret
        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
        
        if not bondi.active_flag:
            debug('bondi not active - moving forward')
            continue
        
        debug('TWITTER: getting list members')
        tic = time.clock()
        newBondees = BondizApp.useTwitterAPI.getListMembers(twitter, slug='Bondiz', owner_screen_name=bondi.twitter_screen_name)
        toc = time.clock()
        debug('TWITTER: done [' + str(toc-tic) + ' seconds]')        
        
        newBondees_screen_names = [newBondee['screen_name'] for newBondee in newBondees]
        
        for oldBondee in bondi.bondee_set.all():
            if not str(oldBondee) in [str(newBondee['screen_name']) for newBondee in newBondees]:
                debug('deleting ' + oldBondee.twitter_screen_name)    
                bondi.realtime_log_set.filter(bondee_screen_name = oldBondee.twitter_screen_name).delete()
                bondi.daily_log_set.filter(bondee_screen_name = oldBondee.twitter_screen_name).delete()
                bondi.bondee_set.filter(twitter_screen_name = oldBondee.twitter_screen_name).delete()
        
        newConnections = []        
        for newBondee in newBondees:
            debug('iterating through bondees (' + newBondee['screen_name'] + ')')
            
            OldBondee = bondi.bondee_set.filter(twitter_screen_name = newBondee['screen_name'])
            
            if not OldBondee:
                
                debug('creating ' + newBondee['screen_name'])
                
                if not newConnections:  
                    debug('TWITTER: getting frienships')
                    tic = time.clock()
                    newConnections = BondizApp.useTwitterAPI.friendship_byNAME(twitter,screen_name = (",".join(newBondees_screen_names)))
                    toc = time.clock()
                
                for newConnection in newConnections:
                    if newConnection['screen_name'] == newBondee['screen_name']:
                        new_follows_me_flag = u'followed_by' in newConnection['connections'] 
                        break               
                
                debug('TWITTER: done [' + str(toc-tic) + ' seconds]') 
                bondi.bondee_set.create(twitter_screen_name = newBondee['screen_name'],
                                        name = newBondee['name'],
                                        image_url = newBondee['profile_image_url'],
                                        followers_num = newBondee['followers_count'],
                                        friends_num = newBondee['friends_count'],                                    
                                        profile_bio = newBondee['description'],
                                        follows_me_flag = new_follows_me_flag)
                
                                                       
                                                
        
        MINUTES_PARAMETER = 10
        POP_MAX_RT = 0
        POP_MAX_FAV = 0
        KEY_MAX_RT = 0
        KEY_MAX_FAV = 0        
        bondiList = bondi.list_set.all()[0]
        
        count = 200
        trim_user = 0
        exclude_replies = 0
        include_rts = 0
        
        debug('TWITTER: getting List Timeline (tweets)')
        tic = time.clock()
        tweets = BondizApp.useTwitterAPI.ListTimeline(twitter,'Bondiz',bondi.twitter_screen_name,count,trim_user,exclude_replies ,include_rts)        
        toc = time.clock()
        debug('TWITTER: done [' + str(toc-tic) + ' seconds]')         
        
        realtime_popular_time_period = int(RtPopTimeTable[bondiList.realtime_popular_time_period])        
        realtime_popular_RT_threshold = int(RtPopMinRTtable[bondiList.realtime_popular_RT_threshold])        
        realtime_popular_FAV_threshold = int(RtPopMinFAVtable[bondiList.realtime_popular_FAV_threshold])

        POP_RTcount = 0
        POP_FAVcount = 0      
        KEY_RTcount = 0
        KEY_FAVcount = 0           
        if len(tweets) > 0:
            for tweet in tweets:
                debug('iterating through tweets (' + tweet['id_str'] + ')')
                timeDelta = datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                if (timeDelta.total_seconds() > realtime_popular_time_period * 60) and (timeDelta.total_seconds() > MINUTES_PARAMETER * 60): 
                # tweet is irrelevant by time created  
                    continue
                
                ### POPULAR ###
                if timeDelta.total_seconds() <= realtime_popular_time_period * 60: 
                # tweet is time relevant for "popular" conditions       
                    if (not 'retweeted_status' in tweet.keys()) or (('retweeted_status' in tweet.keys()) and (tweet['retweeted_status']['user']['screen_name'] in newBondees_screen_names)):
                    # tweet was created by a Bondee
                        if (tweet['retweet_count'] >= realtime_popular_RT_threshold) and (not bondi.realtime_log_set.filter(tweet_id=tweet['id_str'], type="RT")):
                        # RT popular & was not emailed as RT popular before
                            if tweet['retweeted']:
                            # RT done by bondi
                                bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                              time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                debug('TWITTER: retweet')
                                tic = time.clock()
                                BondizApp.useTwitterAPI.ReTweet(twitter,tweet['id_str'])
                                toc = time.clock()
                                debug('TWITTER: retweet done [' + str(toc-tic) + ' seconds]')                               
                                
                                POP_RTcount = POP_RTcount + 1                    
                                bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                              time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                                              time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                                              time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                debug('TWITTER: favorite')
                                tic = time.clock()
                                BondizApp.useTwitterAPI.Favorite(twitter,tweet['id_str'])
                                toc = time.clock()
                                debug('TWITTER: favorite done [' + str(toc-tic) + ' seconds]')  
                                                                                           
                                POP_FAVcount = POP_FAVcount + 1                    
                                bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                              time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                                              time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
                                                              type = "FAV",
                                                              value = str(tweet['favorite_count']),
                                                              condition = str(realtime_popular_FAV_threshold),
                                                              tweet_id = tweet['id_str'],
                                                              tweet_text = tweet['text'],
                                                              RT = 0,
                                                              FAV = 0,
                                                              email_timestamp = "")                            
                                
                                
                ### KEYWORDS ###                                                                  
                if timeDelta.total_seconds() <= MINUTES_PARAMETER * 60:
                # tweet is time relevant for "keyword" conditions  
                    keyword_list = [x['keyword'] for x in bondiList.tweet_keyword_set.all().values()]
                    
                    if (any(keyword.lower() in tweet['text'].lower() for keyword in filter(None,keyword_list))) and (not bondi.realtime_log_set.filter(tweet_id=tweet['id_str'], type="KEY").exclude(email_timestamp="")): 
                    # tweet has keywords inside
                    
                        # RT #
                        if tweet['retweeted']:
                        # RT done by bondi
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword.lower() in tweet['text'].lower():
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
                                                                  type = "KEY",
                                                                  value = "",
                                                                  condition = keyword,
                                                                  tweet_id = tweet['id_str'],
                                                                  tweet_text = tweet['text'],
                                                                  RT = 1,
                                                                  FAV = 0,
                                                                  email_timestamp = "")
                        elif bondiList.realtime_keywords_RT_flag and KEY_RTcount < KEY_MAX_RT:                                    
                        # auto RT is enabled & not overdone
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword.lower() in tweet['text'].lower():
                                    debug('TWITTER: retweet')
                                    tic = time.clock()
                                    BondizApp.useTwitterAPI.ReTweet(twitter,tweet['id_str'])
                                    toc = time.clock()
                                    debug('TWITTER: retweet done [' + str(toc-tic) + ' seconds]')                                      
                                    
                                    KEY_RTcount = KEY_RTcount + 1 
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                if keyword.lower() in tweet['text'].lower():
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                if keyword.lower() in tweet['text'].lower():
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
                                                                  type = "KEY",
                                                                  value = "",
                                                                  condition = keyword,
                                                                  tweet_id = tweet['id_str'],
                                                                  tweet_text = tweet['text'],
                                                                  RT = 0,
                                                                  FAV = 1,
                                                                  email_timestamp = "")
                        elif bondiList.realtime_keywords_FAV_flag and KEY_FAVcount < KEY_MAX_FAV:                                    
                        # auto FAV is enabled & not overdone
                            for keyword in filter(None,keyword_list):
                            # check for indiviual keywords in the tweet
                                if keyword.lower() in tweet['text'].lower():                                    
                                    debug('TWITTER: favorite')
                                    tic = time.clock()
                                    BondizApp.useTwitterAPI.Favorite(twitter,tweet['id_str'])
                                    toc = time.clock()
                                    debug('TWITTER: favorite done [' + str(toc-tic) + ' seconds]')  
                                                                    
                                    KEY_FAVcount = KEY_FAVcount + 1 
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
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
                                if keyword.lower() in tweet['text'].lower():
                                    bondi.realtime_log_set.create(bondee_screen_name = tweet['user']['screen_name'],
                                                                  time = (datetime.utcnow() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()/60,
                                                                  type = "KEY",
                                                                  value = "",
                                                                  condition = keyword,
                                                                  tweet_id = tweet['id_str'],
                                                                  tweet_text = tweet['text'],
                                                                  RT = 0,
                                                                  FAV = 0,
                                                                  email_timestamp = "")                                                                                           
                    
        debug('calling emailTask')
        tic = time.clock()
        emailTask.runEmailTask()
        toc = time.clock()
        debug('emailTask done [' + str(toc-tic) + ' seconds]')                  
        
    return 1

if __name__=='__main__':
    tic = time.clock()
    runRealtimeTask() 
    toc = time.clock()
    debug('RealtimeTask done ['+ str(toc-tic) + ' seconds]')