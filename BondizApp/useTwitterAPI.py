from twython import Twython, TwythonError, TwythonRateLimitError
from taskDebug import taskDebug 
import time

def twitter_retry(func):
    howmany = 2 # maximum retires
    simple_timeout = 1 # seconds
    rate_limit_timeout = 300 # seconds
    def tryIt(*fargs, **fkwargs):
        for _ in xrange(howmany):
            try: return func(*fargs, **fkwargs)
            except (TwythonError, TwythonRateLimitError, Exception) as e:
                if "Rate limit" in str(e): 
                    taskDebug('!!! ' + str(e))
                    #print fkwargs['limit_rate_string']
                    #print 'sleeping for ' + str(rate_limit_timeout) + ' seconds'
                    time.sleep(rate_limit_timeout)
                else:
                    taskDebug('!!! ' + str(e))
                    #print 'sleeping for ' + str(simple_timeout) + ' seconds'
                    time.sleep(simple_timeout)
    return tryIt  
    
@twitter_retry
def twitterGetFollowersIds(twitter,**params):
    return twitter.get_followers_ids(**params)

@twitter_retry
def twitterGetFollowingIds(twitter,**params):
    return twitter.get_friends_ids(**params)    
    
@twitter_retry
def twitterLookupUser(twitter,**params):
    return twitter.lookup_user(**params)

@twitter_retry
def twitterCreateFriendship(twitter,**params):
    return twitter.create_friendship(**params)

@twitter_retry
def twitterDestroyFriendship(twitter,**params):
    return twitter.destroy_friendship(**params)

@twitter_retry
def twitterLookupFriendships(twitter,**params):
    return twitter.lookup_friendships(**params)

@twitter_retry
def twitterRateLimit(twitter,**params):
    return twitter.get_application_rate_limit_status(**params)

@twitter_retry
def twitterReTweet(twitter,**params):
    return twitter.retweet(**params)

@twitter_retry
def twitterFavorite(twitter,**params):
    return twitter.create_favorite(**params)


@twitter_retry
def twitterUserTimeline(twitter,**params):
    return twitter.get_user_timeline(**params)

@twitter_retry
def twitterHomeTimeline(twitter,**params):
    return twitter.get_home_timeline(**params)

@twitter_retry
def twitterDeleteTweet(twitter,**params):
    return twitter.destroy_status(**params)

@twitter_retry
def twitterGetOwnedLists(twitter,**params):
    return twitter.show_owned_lists(**params)

@twitter_retry
def twitterCreateList(twitter,**params):
    return twitter.create_list(**params)

@twitter_retry
def twitterGetListMembers(twitter,**params):
    return twitter.get_list_members(**params)

@twitter_retry
def twitterListTimeline(twitter,**params):
    return twitter.get_list_statuses(**params)

@twitter_retry
def twitterCreateListMembers(twitter,**params):
    return twitter.create_list_members(**params)

@twitter_retry
def twitterDeleteListMembers(twitter,**params):
    return twitter.delete_list_members(**params)


### *********************************************** ###

def getFollowersIds(twitter,subjectScreenName):
#     print '*** getting the followers of ' + subjectScreenName
    ii = 1
#     print 'page ' + str(ii) 
    followersIds_raw = twitterGetFollowersIds(twitter,limit_rate_string='xxx',screen_name=subjectScreenName,cursor=-1,count=5000)
    followersIds_next_cursor = followersIds_raw['next_cursor']
    followersIds_ids = followersIds_raw['ids']
    while followersIds_next_cursor:
        ii += 1
#        print 'page ' + str(ii) 
        followersIds_raw = twitterGetFollowersIds(twitter,limit_rate_string='xxx',screen_name=subjectScreenName,cursor=followersIds_next_cursor,count=5000)
        followersIds_next_cursor = followersIds_raw['next_cursor']
        followersIds_ids = followersIds_ids + followersIds_raw['ids']    
    return followersIds_ids
    
def getFollowingIds(twitter,subjectScreenName):
#     print '*** getting the following of ' + subjectScreenName
    ii = 1
#     print 'page ' + str(ii) 
    followingIds_raw = twitterGetFollowingIds(twitter,screen_name=subjectScreenName,cursor=-1,count=5000)
    followingIds_next_cursor = followingIds_raw['next_cursor']
    followingIds_ids = followingIds_raw['ids']
    while followingIds_next_cursor:
        ii += 1
#        print 'page ' + str(ii)     
        followingIds_raw = twitterGetFollowingIds(twitter,screen_name=subjectScreenName,cursor=followingIds_next_cursor,count=5000)
        followingIds_next_cursor = followingIds_raw['next_cursor']
        followingIds_ids = followingIds_ids + followingIds_raw['ids']    
    return followingIds_ids    

def lookup_byID(twitter, userId):
    return twitterLookupUser(twitter,user_id=userId)

def lookup_byNAME(twitter, screen_name):
    return twitterLookupUser(twitter,screen_name=screen_name)

def followUser(twitter, subjectName):
#    print '*** following ' + subjectName
    return twitterCreateFriendship(twitter,screen_name=subjectName)   

def followUser_byID(twitter, userId):
#    print '*** following ' + userId
    return twitterCreateFriendship(twitter,user_id=userId)    

def followUser_byNAME(twitter, screen_name):
#    print '*** following ' + screen_name
    return twitterCreateFriendship(twitter,screen_name=screen_name)  
    
def unfollowUser_byID(twitter, userId):
#    print '*** unfollowing ' + userId
    return twitterDestroyFriendship(twitter,user_id=userId)  
    
def friendship_byID(twitter, userId):
    return twitterLookupFriendships(twitter,user_id=userId) 

def friendship_byNAME(twitter, screen_name):
    return twitterLookupFriendships(twitter,screen_name=screen_name)         
    
def getRateLimit(twitter, resources):    
    return twitterRateLimit(twitter,resources=resources)

def ReTweet(twitter, tweetId):    
    return twitterReTweet(twitter,id=tweetId)
 
def Favorite(twitter, tweetId):    
    return twitterFavorite(twitter,id=tweetId)    
    
def UserTimeline(twitter,screen_name,count,trim_user,exclude_replies ,include_rts):
#     print '*** getting UserTimeline of ' + screen_name
    ii = 1
#     print 'page ' + str(ii) 
    UserTimeline_raw = twitterUserTimeline(twitter,screen_name=screen_name,count=count,trim_user=trim_user,exclude_replies=exclude_replies,include_rts=include_rts)
    UserTimeline = [] 
    while len(UserTimeline_raw) > 0:
        ii += 1
#         print 'page ' + str(ii)          
        UserTimeline = UserTimeline + UserTimeline_raw
        UserTimeline_max_id = int(UserTimeline_raw[-1]['id'])-1        
        UserTimeline_raw = twitterUserTimeline(twitter,max_id=UserTimeline_max_id,screen_name=screen_name,count=count,trim_user=trim_user,exclude_replies=exclude_replies,include_rts=include_rts)  
    return UserTimeline

#def HomeTimeline(twitter,screen_name,count,trim_user,exclude_replies ,include_rts):
    #print '*** getting HomeTimeline of ' + screen_name
    #ii = 1
    #print 'page ' + str(ii) 
    #HomeTimeline_raw = twitterHomeTimeline(twitter,screen_name=screen_name,count=count,trim_user=trim_user,exclude_replies=exclude_replies,include_rts=include_rts)
    #HomeTimeline = [] 
    #while len(HomeTimeline_raw) > 0:
        #ii += 1
        #print 'page ' + str(ii)          
        #HomeTimeline = HomeTimeline + HomeTimeline_raw
        #HomeTimeline_max_id = int(HomeTimeline_raw[-1]['id'])-1        
        #HomeTimeline_raw = twitterHomeTimeline(twitter,max_id=HomeTimeline_max_id,screen_name=screen_name,count=count,trim_user=trim_user,exclude_replies=exclude_replies,include_rts=include_rts)  
#    return HomeTimeline

# getting only ONE Home Timeline
def HomeTimeline(twitter,screen_name,count,trim_user,exclude_replies ,include_rts):
#     print '*** getting ONE! HomeTimeline of ' + screen_name
    HomeTimeline = twitterHomeTimeline(twitter,screen_name=screen_name,count=count,trim_user=trim_user,exclude_replies=exclude_replies,include_rts=include_rts)
    return HomeTimeline

def DeleteTweet(twitter, tweetId):    
    return twitterDeleteTweet(twitter,id=tweetId)

def getOwnedLists(twitter, screen_name):    
    return twitterGetOwnedLists(twitter,screen_name=screen_name)

def createList(twitter, name, mode):    
    return twitterCreateList(twitter,name=name,mode=mode)

def getListMembers(twitter, slug, owner_screen_name):     
#     print '*** getting "Bondiz" list members of ' + owner_screen_name
    ii = 1
#     print 'page ' + str(ii) 
    members_raw = twitterGetListMembers(twitter,slug=slug,owner_screen_name=owner_screen_name,cursor=-1)
    members_next_cursor = members_raw['next_cursor']
    members_names = members_raw['users']
    while members_next_cursor:
        ii += 1
#         print 'page ' + str(ii) 
        members_raw = twitterGetListMembers(twitter,slug=slug,owner_screen_name=owner_screen_name,cursor=members_next_cursor)
        members_next_cursor = members_raw['next_cursor']
        members_names = members_names + members_raw['users']    
    return members_names

def ListTimeline(twitter,slug,owner_screen_name,count,trim_user,exclude_replies ,include_rts):    
    #print '*** getting ONE! ListTimeline of ' + owner_screen_name
    HomeTimeline = twitterListTimeline(twitter,slug=slug,owner_screen_name=owner_screen_name,count=count,trim_user=trim_user,exclude_replies=exclude_replies,include_rts=include_rts)
    return HomeTimeline

def CreateListMembers(twitter,owner_screen_name,slug,screen_name):    
    res = twitterCreateListMembers(twitter,owner_screen_name=owner_screen_name,slug=slug,screen_name=screen_name)
    return res    

def DeleteListMembers(twitter,owner_screen_name,slug,screen_name):    
    res = twitterDeleteListMembers(twitter,owner_screen_name=owner_screen_name,slug=slug,screen_name=screen_name)
    return res   
    