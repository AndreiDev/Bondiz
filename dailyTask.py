#cd /home/andreii1/django_projects/Bondiz && /home/andreii1/python/bin/python dailyTask.py

#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bondiz.settings")
import Bondiz.settings

import emailTask
from BondizApp.models import Bondi, List, Tweet_keyword, Bondee, Daily_log
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

def runDailyTask():
    debug('****** runDailyTask started ******')
    for bondi in Bondi.objects.all():
        try:
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
            if not bondi.list_set.all()[0].active_flag:
                debug('list not active - moving forward')
                continue            
            
            bondiList = bondi.list_set.all()[0]
            report_followers_num = bondiList.report_followers_num  
            report_friends_num = bondiList.report_friends_num    
                 
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
            
            debug('TWITTER: getting friendships')
            tic = time.clock()
            newConnections = BondizApp.useTwitterAPI.friendship_byNAME(twitter,screen_name = (",".join(newBondees_screen_names)))
            toc = time.clock()    
            debug('TWITTER: done [' + str(toc-tic) + ' seconds]')     
                  
            for newBondee in newBondees:
                try:
                    #debug('iterating through bondees (' + newBondee['screen_name'] + ')')
                    
                    for newConnection in newConnections:
                        if newConnection['screen_name'] == newBondee['screen_name']:
                            new_follows_me_flag = u'followed_by' in newConnection['connections'] 
                            break              
                    
                    OldBondee = bondi.bondee_set.filter(twitter_screen_name = newBondee['screen_name'])
                    
                    if not OldBondee:
                        
                        debug('creating ' + newBondee['screen_name'])                        
                                                
                        bondi.bondee_set.create(twitter_screen_name = newBondee['screen_name'],
                                                name = newBondee['name'],
                                                image_url = newBondee['profile_image_url'],
                                                followers_num = newBondee['followers_count'],
                                                friends_num = newBondee['friends_count'],                                    
                                                profile_bio = newBondee['description'],
                                                follows_me_flag = new_follows_me_flag)
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
                    newSnapshot['relationship'] = new_follows_me_flag     
        
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
                except Exception as e:   
                    debug('!!! Exception in ' + newBondee['screen_name'] + ': ' + str(e))                                                                              
        except Exception as e:   
            debug('!!! Exception in ' + bondi.twitter_screen_name + ': ' + str(e))
    return 1

if __name__=='__main__':
    tic = time.clock()
    runDailyTask() 
    toc = time.clock()
    debug('------ DailyTask done ['+ str(toc-tic) + ' seconds] ------')