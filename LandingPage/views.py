from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from models import Log

def homepage(request):
    newLog = Log(ip=request.META['REMOTE_ADDR'],text='homepage')
    newLog.save()
    return render_to_response('LandingPage/index.html',context_instance=RequestContext(request))

def plans(request):
    newLog = Log(ip=request.META['REMOTE_ADDR'],text='plans')
    newLog.save()    
    return render_to_response('LandingPage/pricing-plans.html',context_instance=RequestContext(request))    
    
def signup(request):
    newLog = Log(ip=request.META['REMOTE_ADDR'],text="signup")
    newLog.save()
    return render_to_response('LandingPage/signup.html',context_instance=RequestContext(request))      

def thanks(request):
    if not request.POST.values():
        return render_to_response('LandingPage/thanks.html',context_instance=RequestContext(request))
    if not request.POST.values()[1]:
        return redirect("/signup")
    else:
        newLog = Log(ip=request.META['REMOTE_ADDR'],text=request.POST.values()[1])
        newLog.save()    
        return render_to_response('LandingPage/thanks.html',context_instance=RequestContext(request))
        