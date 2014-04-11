import time

def profile_retry(func):
    howmany = 10 # maximum retires
    timeout = 3 # seconds
    def tryIt(*fargs, **fkwargs):
        for _ in xrange(howmany):
            try: return func(*fargs, **fkwargs)
            except (Exception) as e:
                print e
                print 'sleeping for ' + str(timeout) + ' seconds'
                time.sleep(timeout)
    return tryIt  

@profile_retry
def getUserProfile(userName):
    import urllib
    import re

    url = 'https://twitter.com/' + str(userName)
    response = urllib.urlopen(url).read()
    match = re.findall(r'ollow.*<strong title=".*">(.*)</strong>',response)
    if match:
        picAndName = re.findall(r'<img src="(.*)" alt="(.*)" class',response)
        pic = picAndName[0][0]
        name = picAndName[0][1]
        tweets = cleanNum(re.findall(r'weet.*<strong title=".*">(.*)</strong>',response)[0])
        following = cleanNum(match[0])
        followers = cleanNum(match[1])
        isBlocked = len(re.findall(r'data-protected="true"',response))
        if not isBlocked:
            return [name, pic, tweets, following, followers]
        else:
            return ''
    else: 
        return ''
    
def cleanNum(rawNum):
    Num = rawNum.replace(',','')
    if '.' in Num:
        return Num.replace('.','').replace('K','00')
    else:
        return Num.replace('K','000')
    