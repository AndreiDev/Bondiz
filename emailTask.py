#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bondiz.settings")
import Bondiz.settings

from BondizApp.models import Stalk_task
import time
from emailDebug import emailDebug
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
    emailDebug('***  runEmailTask started ***')
    for task in Stalk_task.objects.filter(sent_flag=False).exclude(tweet_id=""):
        
        emailContext = Context({'username':task.target_username,'tweet_id': task.tweet_id,'tweet_text': task.tweet_text})
        plaintext = get_template('../templates/email/email.txt')
        htmly     = get_template('../templates/email/email.html')
        subject, from_email, to = 'Heads up - @' + task.target_username + ' just tweeted', 'headsup@bondiz.com', task.email
        text_content = plaintext.render(emailContext)
        html_content = htmly.render(emailContext)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        
        emailDebug('DJANGO: sending email')
        tic = time.clock()
        msg.send()    
        toc = time.clock()
        emailDebug('DJANGO: done [' + str(toc-tic) + ' seconds]') 
        
        task.sent_flag = True
        task.save()        
        
    return 1

if __name__=='__main__':
    tic = time.clock()
    runEmailTask() 
    toc = time.clock()
    emailDebug('---  runEmailTask done ['+ str(toc) + ' seconds] ---')