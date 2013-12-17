import json
from dajaxice.decorators import dajaxice_register
from models import Stalk_task
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI
from getUserProfile import getUserProfile
from datetime import datetime,timedelta

@dajaxice_register
def AJ_go(request, username, email):
    
    if Stalk_task.objects.filter(target_username=username, email=email, tweet_id=""):
        return json.dumps({'res':'91'})
    
    if len(Stalk_task.objects.filter(email=email, tweet_id="")) > 4:
        return json.dumps({'res':'93'})
    
    APP_KEY = 'kOzrNIHIZm5nZi4ONNV2eg'
    APP_SECRET = 'NXFxZ1GA76zknOVR5VdOv87rHNpcI1mM0DxZyvYEvt0'
    OAUTH_TOKEN = '720312389-aCHgpGK63aBdCizeEXi7DLkoeYhBePQAPOcqOsgX'
    OAUTH_TOKEN_SECRET = 'iOKitaWhDJ3NMrWRkgLpoGuAh1OrzUliQgPA0EdU'
    
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    owner_screen_name = "Bondiz"
    slug = "Bondiz"
    
    screen_name = username
    
    userProfile = getUserProfile(username)
    
    if not userProfile:
        return json.dumps({'res':'92'})
    
    if Stalk_task.objects.filter(target_username=username,tweet_id=""):
        res = 1
    else:
        res = useTwitterAPI.CreateListMembers(twitter,owner_screen_name,slug,screen_name)
    
    if res:
        newStalkTask = Stalk_task(target_username=screen_name, email=email, created_at = datetime.utcnow())
        newStalkTask.save() 
        return json.dumps({'res':'1'})
    else:
        return json.dumps({'res':'90'})