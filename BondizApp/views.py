from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Stalk_task
#from django.shortcuts import redirect

#import useTwitterAPI
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI
    
def home(request):
    return render_to_response('BondizApp/home.html',context_instance=RequestContext(request))  


# Paypal section
import paypalrestsdk

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from Bondiz.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET

def paypal_create(request):
    """
    MyApp > Paypal > Create a Payment
    """
    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal" },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('BondizApp.views.paypal_execute')),
            "cancel_url": request.build_absolute_uri(reverse('BondizApp.views.home')) },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Bondiz",
                    "price": "1",
                    "currency": "USD",
                    "quantity": 1 }]},
            "amount":  {
                "total": "1",
                "currency": "USD" },
            "description": "1 Bondiz" }]})

    redirect_url = ""

    if payment.create():
        # Store payment id in user session
        request.session['payment_id'] = payment.id

        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
        return HttpResponseRedirect(redirect_url)

    else:
        messages.error(request, 'We are sorry but something went wrong. We could not redirect you to Paypal.')
        return HttpResponseRedirect(reverse('BondizApp.views.home'))   
    
def paypal_execute(request):
    """
    MyApp > Paypal > Execute a Payment
    """
    
    if not 'PayerID' in request.GET:
        return render_to_response('BondizApp/purchase.html',context_instance=RequestContext(request,{'caption': 'Naaa'}))
    
    payment_id = request.session['payment_id']
    payer_id = request.GET['PayerID']
     
    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment.find(payment_id)
    payment_name = payment.transactions[0].item_list.items[0].name

    if payment.execute({"payer_id": payer_id}):
        return render_to_response('BondizApp/purchase.html',context_instance=RequestContext(request,{'caption': 'OK'}))
    else:
        return render_to_response('BondizApp/purchase.html',context_instance=RequestContext(request,{'caption': 'Naaa'}))

    return HttpResponseRedirect(reverse('BondizApp.views.home'))     


# Classic Paypal stuff
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse

def success(request):
    return render_to_response('BondizApp/purchase.html',context_instance=RequestContext(request,{'caption': 'SUCCESS'}))

def cancel(request):
    return render_to_response('BondizApp/purchase.html',context_instance=RequestContext(request,{'caption': 'CANCEL'}))

def paypal(request):

    # What you want the button to do.

    paypal_dict = {
                   "cmd": "_xclick-subscriptions",
                   "a1": "0",     # trial price 
                   "p1": 1,     # trial duration, duration of unit defaults to month 
                   "a3": "29.95", # yearly price 
                   "p3": 1, # duration of each unit (depends on unit) 
                   "t3": "Y", # duration unit ("M for Month") 
                   "src": "1", # make payments recur 
                   "sra": "1", # reattempt payment on payment error 
                   "no_note": "1", # remove extra notes (optional)        
        
                   "business": settings.PAYPAL_RECEIVER_EMAIL,
                   "amount": "1.00",
                   "item_name": "one Bondiz",
                   "invoice": "101",
                   "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
                   "return_url": "http://www.bondiz.com/success/",
                   "cancel_return": "http://www.bondiz.com/cancel/",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe") 
    context = {"form": form.sandbox()} # form.render() for real case
    return render_to_response("paypal.html", context)

from paypal.standard.ipn.signals import payment_was_successful

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    if ipn_obj.custom == "Upgrade all users!":
        Users.objects.update(paid=True)
    print __file__,1, 'This works'        
payment_was_successful.connect(show_me_the_money)