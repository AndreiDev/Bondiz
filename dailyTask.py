#from django.core.management import setup_environ
import Bondiz.settings
#setup_environ(CrossValidate.settings)
import emailTask
from BondizApp.models import Bondi, List, Tweet_keyword, Bondee, Daily_log
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

def runDailyTask():
    RepFollowersNumTable = {1:u'2',2:u'5',3:u'10',4:u'30',5:u'50'}
    RepFriendsNumTable = {1:u'2',2:u'5',3:u'10',4:u'30',5:u'50'}

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
        
        bondiList = bondi.list_set.all()[0]
        report_followers_num = int(RepFollowersNumTable[bondiList.report_followers_num])   
        report_friends_num = int(RepFriendsNumTable[bondiList.report_friends_num])      
             
        newBondees = BondizApp.useTwitterAPI.getListMembers(twitter, slug='Bondiz', owner_screen_name=bondi.twitter_screen_name)
        
        for oldBondee in bondi.bondee_set.all():
            if not str(oldBondee) in [str(newBondee['screen_name']) for newBondee in newBondees]:
                bondi.realtime_log_set.filter(bondee_screen_name = oldBondee.twitter_screen_name).delete()
                bondi.daily_log_set.filter(bondee_screen_name = oldBondee.twitter_screen_name).delete()
                bondi.bondee_set.filter(twitter_screen_name = oldBondee.twitter_screen_name).delete()
                
        for newBondee in newBondees:
            
            OldBondee = bondi.bondee_set.filter(twitter_screen_name = newBondee['screen_name'])
            
            if not OldBondee:
                bondi.bondee_set.create(twitter_screen_name = newBondee['screen_name'],
                                        name = newBondee['name'],
                                        image_url = newBondee['profile_image_url'],
                                        followers_num = newBondee['followers_count'],
                                        friends_num = newBondee['friends_count'],                                    
                                        profile_bio = newBondee['description'],
                                        follows_me_flag = u'followed_by' in BondizApp.useTwitterAPI.friendship_byNAME(twitter,screen_name = newBondee['screen_name'])[0]['connections'])
                continue
            else:
                OldBondee = OldBondee[0]
            
            oldSnapshot = {}
            oldSnapshot['followersNum'] = OldBondee.followers_num
            oldSnapshot['friendsNum'] = OldBondee.friends_num
            oldSnapshot['bio'] = OldBondee.profile_bio
            oldSnapshot['relationship'] = OldBondee.follows_me_flag
            
            newSnapshot = {}
            newSnapshot['followersNum'] = newBondee['followers_count']
            newSnapshot['friendsNum'] = newBondee['friends_count']
            newSnapshot['bio'] = newBondee['description']
            newSnapshot['relationship'] = u'followed_by' in BondizApp.useTwitterAPI.friendship_byNAME(twitter,screen_name = newBondee['screen_name'])[0]['connections']
                
            if newSnapshot['followersNum'] - oldSnapshot['followersNum'] >= report_followers_num:
            # following growth
                bondi.daily_log_set.create(bondee_screen_name = newBondee['screen_name'],
                                          type = "FOLLOWERS",
                                          before = oldSnapshot['followersNum'],
                                          after = newSnapshot['followersNum'],
                                          email_timestamp = "")  
                OldBondee.followers_num = newSnapshot['followersNum']
                OldBondee.save() 
            if newSnapshot['friendsNum'] - oldSnapshot['friendsNum'] >= report_friends_num:
            # followers growth
                bondi.daily_log_set.create(bondee_screen_name = newBondee['screen_name'],
                                          type = "FRIENDS",
                                          before = oldSnapshot['friendsNum'],
                                          after = newSnapshot['friendsNum'],
                                          email_timestamp = "")   
                OldBondee.friends_num = newSnapshot['friendsNum']
                OldBondee.save()                 
            if newSnapshot['bio'] != oldSnapshot['bio']:
            # bio change
                bondi.daily_log_set.create(bondee_screen_name = newBondee['screen_name'],
                                          type = "BIO",
                                          before = oldSnapshot['bio'],
                                          after = newSnapshot['bio'],
                                          email_timestamp = "")
                OldBondee.profile_bio = newSnapshot['bio']
                OldBondee.save()                 
            if newSnapshot['relationship'] != oldSnapshot['relationship']:
            # relationship change
                bondi.daily_log_set.create(bondee_screen_name = newBondee['screen_name'],
                                          type = "RELATIONSHIP",
                                          before = oldSnapshot['relationship'],
                                          after = newSnapshot['relationship'],
                                          email_timestamp = "")
                OldBondee.follows_me_flag = newSnapshot['relationship']  
                OldBondee.save()                                                               

    return 1

if __name__=='__main__':
    tic = time.clock()
    runDailyTask() 
    toc = time.clock()
    print ['RealtimeTask done in '+ str(toc) + ' seconds']