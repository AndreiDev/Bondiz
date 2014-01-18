#cd /home/andreii1/django_projects/Bondiz && /home/andreii1/python/bin/python realtimeTask.py

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bondiz.settings")
import Bondiz.settings

from BondizApp.models import Stalk_task
import time
from taskDebug import taskDebug
import BondizApp.useTwitterAPI
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
from django.contrib.auth.models import User
import datetime
import time
from django.utils.timezone import utc
from datetime import datetime,timedelta
#from BondizApp.ajax import

def runRealtimeTask():
    taskDebug('*** RealtimeTask started ***') 
    try:
    
        APP_KEY = 'kOzrNIHIZm5nZi4ONNV2eg'
        APP_SECRET = 'NXFxZ1GA76zknOVR5VdOv87rHNpcI1mM0DxZyvYEvt0'
        OAUTH_TOKEN = '720312389-aCHgpGK63aBdCizeEXi7DLkoeYhBePQAPOcqOsgX'
        OAUTH_TOKEN_SECRET = 'iOKitaWhDJ3NMrWRkgLpoGuAh1OrzUliQgPA0EdU'
        
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        count = 200
        trim_user = 0
        exclude_replies = 0
        include_rts = 0            
            
        taskDebug('TWITTER: getting List Timeline (tweets)')
        tic = time.clock()
        tweets = BondizApp.useTwitterAPI.ListTimeline(twitter,'Bondiz','Bondiz',count,trim_user,exclude_replies ,include_rts)        
        toc = time.clock()
        taskDebug('TWITTER: done [' + str(toc-tic) + ' seconds]')         
        
        for tweet in tweets:
            for task in Stalk_task.objects.filter(target_username = tweet['user']['screen_name'].lower(),tweet_id=""):
                if (datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') - task.created_at).total_seconds() > 0:
                    task.tweet_id = tweet['id_str']
                    task.tweet_text = tweet['text']
                    task.save()
                                        
                    if not Stalk_task.objects.filter(target_username=tweet['user']['screen_name'].lower(),tweet_id=""):
                        owner_screen_name = "Bondiz"
                        slug = "Bondiz"
                        screen_name = tweet['user']['screen_name']    
                        res = BondizApp.useTwitterAPI.DeleteListMembers(twitter,owner_screen_name,slug,screen_name)
                                                
    except Exception as e:   
            taskDebug('!!! Exception in runRealtimeTask : ' + str(e))    
    return 1

if __name__=='__main__':
    tic = time.clock()
    runRealtimeTask() 
    toc = time.clock()
    taskDebug('--- RealtimeTask done ['+ str(toc-tic) + ' seconds] ---')