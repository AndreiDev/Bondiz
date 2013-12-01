#from django.core.management import setup_environ
import Bondiz.settings
#setup_environ(CrossValidate.settings)

from BondizApp.models import Bondi, List, Tweet_keyword, Bondee, Realtime_log, Daily_log
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

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def runEmailTask():
 
    for bondi in Bondi.objects.all():
        realtime_logs = bondi.realtime_log_set.filter(email_timestamp="")
        daily_logs = bondi.daily_log_set.filter(email_timestamp="")        
               
        dailyEmailHeading = [] 
        dailyEmailContent = []        
        if daily_logs:        
            dailyEmailHeading = "Daily events:" 
            for daily_log in daily_logs: 
                text = ""
                if daily_log.type == "FOLLOWERS":
                    text = "Number of followers grew from " + daily_log.before + " to " + daily_log.after + "."
                elif daily_log.type == "FRIENDS":
                    text = "Number of friends grew from " + daily_log.before + " to " + daily_log.after + "."
                elif daily_log.type == "RELATIONSHIP":
                    if (daily_log.before == False) and (daily_log.after == True):
                        text = "Now following you."
                    if (daily_log.before == True) and (daily_log.after == False):
                        text = "Not following you anymore."
                elif daily_log.type == "BIO":
                    text = "Changed his profile bio from:'" + daily_log.before + "' to: '" + daily_log.after + "'."                                            
                
                dailyEmailContent = dailyEmailContent + [{'image_url':bondi.bondee_set.filter(twitter_screen_name=daily_log.bondee_screen_name)[0].image_url,
                                                         'screen_name':daily_log.bondee_screen_name,
                                                         'name':bondi.bondee_set.filter(twitter_screen_name=daily_log.bondee_screen_name)[0].name,
                                                         'text':text}]                
                
                daily_log.email_timestamp = str(int(time.time()))
                daily_log.save() 
                
        realtimeEmailHeading = [] 
        realtimeEmailContent = []    
        if realtime_logs:
            realtimeEmailHeading = "Realtime events:"
            for realtime_log in realtime_logs:        
                text = ""
                
                if realtime_log.type == "KEY":
                    text = "Mentioned '" + realtime_log.condition + "' in: '" + realtime_log.tweet_text + "'."                     
                elif realtime_log.type == "RT":
                    text = "Got retweeted " + realtime_log.value + " times (minimum set on " + realtime_log.condition + ") with: '" + realtime_log.tweet_text + "'."                
                elif realtime_log.type == "FAV":
                    text = "Got favorited " + realtime_log.value + " times (minimum set on " + realtime_log.condition + ") with: '" + realtime_log.tweet_text + "'."     
                if realtime_log.RT == 2:
                    text = text + " Auto Retweeted!"
                if realtime_log.FAV == 2:
                    text = text + " Auto Favorited!"  
                                                     
                realtimeEmailContent = realtimeEmailContent + [{'image_url':bondi.bondee_set.filter(twitter_screen_name=realtime_log.bondee_screen_name)[0].image_url,
                                                               'screen_name':realtime_log.bondee_screen_name,
                                                               'name':bondi.bondee_set.filter(twitter_screen_name=realtime_log.bondee_screen_name)[0].name,
                                                               'text':text,
                                                               'tweet_id':realtime_log.tweet_id}]                  
                          
                realtime_log.email_timestamp = str(int(time.time()))
                realtime_log.save()
        
        if dailyEmailContent or realtimeEmailContent:         
            emailContext = Context({'bondi':bondi.twitter_screen_name,'dailyEmailHeading': dailyEmailHeading,'dailyEmailContent': dailyEmailContent, 'realtimeEmailHeading': realtimeEmailHeading,'realtimeEmailContent': realtimeEmailContent })
            plaintext = get_template('../templates/email/email.txt')
            htmly     = get_template('../templates/email/email.html')
            subject, from_email, to = 'Bondiz notification', 'andrei@bondiz.com', bondi.email
            text_content = plaintext.render(emailContext)
            html_content = htmly.render(emailContext)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()           
            
    return 1

if __name__=='__main__':
    tic = time.clock()
    runEmailTask() 
    toc = time.clock()
    print ['runEmailTask done in '+ str(toc) + ' seconds']