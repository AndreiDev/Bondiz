from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Bondi, Bondi_lists, Bondi_tweet_keywords, Bondi_friends_keywords
#from django.shortcuts import redirect

#import useTwitterAPI
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI
    
def home(request):
    if request.user.is_authenticated():
        bondis = Bondi.objects.filter(twitter_screen_name=request.user)
        SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
        APP_KEY = SocialApp.objects.filter(name='Bondiz')[0].client_id 
        APP_SECRET = SocialApp.objects.filter(name='Bondiz')[0].secret
        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                          
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        if not bondis: # new authenticated user 
            newBondi = Bondi(twitter_screen_name=request.user)
            newBondi.save()            
        
        bondi = Bondi.objects.filter(twitter_screen_name=request.user)[0]
        if not Bondi_lists.objects.filter(bondi=bondi): # user doesn't have "Bondiz" in Bondi_list in DB   
            OwnedLists = useTwitterAPI.getOwnedLists(twitter,request.user)['lists']   
            listNames = {OwnedList['name'] for OwnedList in OwnedLists}    
            if 'Bondiz' not in listNames: # user doesn't have "Bondiz" list in Twitter
                useTwitterAPI.createList(twitter,name='Bondiz',method='private')
            newList = Bondi_lists(bondi=bondi,list_name='Bondiz')
            newList.save()            
                    
        bondiList = Bondi_lists.objects.filter(bondi=bondi)[0]
        bondiTweetKeywords = Bondi_tweet_keywords.objects.filter(bondi_list=bondiList) 
        bondiFriendsKeywords = Bondi_friends_keywords.objects.filter(bondi_list=bondiList)              
        return render_to_response('BondizApp/dashboard.html',{'bondi': bondi,'bondiList': bondiList,'bondiTweetKeywords':bondiTweetKeywords,'bondiFriendsKeywords':bondiFriendsKeywords},context_instance=RequestContext(request))      
                  
    else:        
        return render_to_response('BondizApp/home.html',context_instance=RequestContext(request))   
