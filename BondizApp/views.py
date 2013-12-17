from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Stalk_task
#from django.shortcuts import redirect

#import useTwitterAPI
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI
    
def home(request):
    return render_to_response('BondizApp/home.html',context_instance=RequestContext(request))      