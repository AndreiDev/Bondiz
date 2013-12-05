#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bondiz.settings")
import Bondiz.settings

from BondizApp.models import Bondi, List, Tweet_keyword, Bondee, Realtime_log, Daily_log
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

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def runEmailTask():
    debug('runEmailTask started')
    for bondi in Bondi.objects.all():
        realtime_logs = bondi.realtime_log_set.filter(email_timestamp="")
        daily_logs = bondi.daily_log_set.filter(email_timestamp="")        
               
        dailyEmailHeading = [] 
        dailyEmailContent = []        
        if daily_logs:     
            debug('iterating through daily logs...')
               
            dailyEmailHeading = "Daily events:" 
            
            unique_screen_names = list(set([daily_log.bondee_screen_name for daily_log in daily_logs]))
            for unique_screen_name in unique_screen_names:  
                screen_name_daily_logs = daily_logs.filter(bondee_screen_name=unique_screen_name)   
                text = ""
                for screen_name_daily_log in screen_name_daily_logs:                         
                    if screen_name_daily_log.type == "FOLLOWERS":
                        text = text + "Number of followers grew from " + screen_name_daily_log.before + " to " + screen_name_daily_log.after + ". "
                    if screen_name_daily_log.type == "FRIENDS":
                        text = text + "Number of friends grew from " + screen_name_daily_log.before + " to " + screen_name_daily_log.after + ". "
                    if screen_name_daily_log.type == "RELATIONSHIP":
                        if (screen_name_daily_log.before == False) and (screen_name_daily_log.after == True):
                            text = text + "Started following you. "
                        if (screen_name_daily_log.before == True) and (screen_name_daily_log.after == False):
                            text = text + "Not following you anymore. "
                    if screen_name_daily_log.type == "BIO":
                        text = text + "Changed his profile bio from:'" + screen_name_daily_log.before + "' to: '" + screen_name_daily_log.after + "'. "                                            
                    screen_name_daily_log.email_timestamp = str(int(time.time()))
                    screen_name_daily_log.save()                 
                dailyEmailContent = dailyEmailContent + [{'image_url':bondi.bondee_set.filter(twitter_screen_name=screen_name_daily_log.bondee_screen_name)[0].image_url,
                                                         'screen_name':screen_name_daily_log.bondee_screen_name,
                                                         'name':bondi.bondee_set.filter(twitter_screen_name=screen_name_daily_log.bondee_screen_name)[0].name,
                                                         'text':text}]                
                
        realtimeEmailHeading = [] 
        realtimeEmailContent = []    
        if realtime_logs:
            debug('iterating through realtime logs...')
            
            realtimeEmailHeading = "Realtime events:"
            unique_tweet_ids = list(set([realtime_log.tweet_id for realtime_log in realtime_logs]))
            for unique_tweet_id in unique_tweet_ids:  
                tweet_id_realtime_logs = realtime_logs.filter(tweet_id=unique_tweet_id)   
                text = ""
                for tweet_id_realtime_log in tweet_id_realtime_logs:                                           
                    if tweet_id_realtime_log.type == "KEY":
                        if not "Mentioned '" + tweet_id_realtime_log.condition + "'. " in text:
                            text = text + "Mentioned '" + tweet_id_realtime_log.condition + "'. "                                                
                    if tweet_id_realtime_log.type == "RT":
                        text = text + "Got retweeted " + tweet_id_realtime_log.value + " times (minimum set on " + tweet_id_realtime_log.condition + "). "                
                    if tweet_id_realtime_log.type == "FAV":
                        text = text + "Got favorited " + tweet_id_realtime_log.value + " times (minimum set on " + tweet_id_realtime_log.condition + "). "     
                    if tweet_id_realtime_log.RT == 2:
                        text = text + " Auto Retweeted!" 
                    if tweet_id_realtime_log.FAV == 2:
                        text = text + " Auto Favorited! "  
                    tweet_id_realtime_log.email_timestamp = str(int(time.time()))
                    tweet_id_realtime_log.save()                        
                tweet_text = 'Tweet created ' + str(tweet_id_realtime_log.time) + ' minutes ago: "'+ tweet_id_realtime_log.tweet_text +'"'                                         
                realtimeEmailContent = realtimeEmailContent + [{'image_url':bondi.bondee_set.filter(twitter_screen_name=tweet_id_realtime_log.bondee_screen_name)[0].image_url,
                                                               'screen_name':tweet_id_realtime_log.bondee_screen_name,
                                                               'name':bondi.bondee_set.filter(twitter_screen_name=tweet_id_realtime_log.bondee_screen_name)[0].name,
                                                               'text':text,
                                                               'tweet_text':tweet_text,
                                                               'tweet_id':tweet_id_realtime_log.tweet_id}]                  
                          

        if not bondi.email:
            debug('no email defined for @' + bondi.twitter_screen_name)
        else:
            if dailyEmailContent or realtimeEmailContent:         
                emailContext = Context({'bondi':bondi.twitter_screen_name,'dailyEmailHeading': dailyEmailHeading,'dailyEmailContent': dailyEmailContent, 'realtimeEmailHeading': realtimeEmailHeading,'realtimeEmailContent': realtimeEmailContent })
                plaintext = get_template('../templates/email/email.txt')
                htmly     = get_template('../templates/email/email.html')
                subject, from_email, to = 'Bondiz notification', 'andrei@bondiz.com', bondi.email
                text_content = plaintext.render(emailContext)
                html_content = htmly.render(emailContext)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                
                debug('DJANGO: sending email')
                tic = time.clock()
                msg.send()    
                toc = time.clock()
                debug('DJANGO: done [' + str(toc-tic) + ' seconds]')              

    return 1

#if __name__=='__main__':
#    tic = time.clock()
#    runEmailTask() 
#    toc = time.clock()
#    print ['runEmailTask done ['+ str(toc) + ' seconds]']