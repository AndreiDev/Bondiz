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


# Paypal section
import paypalrestsdk

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET

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
                    "price": "5",
                    "currency": "USD",
                    "quantity": 1 }]},
            "amount":  {
                "total": "5",
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