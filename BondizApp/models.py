from django.db import models
from django.core.validators import RegexValidator

class Bondi(models.Model):
    twitter_screen_name = models.CharField(max_length=20,default='')
    
    email = models.CharField(max_length=40,default='')
    plan = models.IntegerField(default=1)
    active_flag = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.twitter_screen_name
    
class Bondi_lists(models.Model):
    bondi = models.ForeignKey(Bondi)
    list_name = models.CharField(max_length=30,default='')

    realtime_keywords_RT_flag = models.BooleanField(default=True)
    realtime_keywords_FAV_flag = models.BooleanField(default=True)
    realtime_popular_RT_flag = models.BooleanField(default=True)
    realtime_popular_FAV_flag = models.BooleanField(default=True)
    realtime_popular_time_period = models.IntegerField(default=20)
    realtime_popular_RT_threshold = models.IntegerField(default=5)
    realtime_popular_FAV_threshold = models.IntegerField(default=5)
    
    report_friends_num = models.IntegerField(default=10)
    rerort_follows_me_flag = models.BooleanField(default=True)
    report_change_bio_flag = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.list_name  
    
class Bondi_tweet_keywords(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    bondi_list = models.ForeignKey(Bondi_lists)
    keyword = models.CharField(max_length=20,default='', validators=[alphanumeric])
    
    def __unicode__(self):
        return self.keyword  
    
class Bondi_friends_keywords(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    bondi_list = models.ForeignKey(Bondi_lists)
    keyword = models.CharField(max_length=20,default='', validators=[alphanumeric])

    def __unicode__(self):
        return self.keyword  
    
class Bondee(models.Model):
    profile_bio = models.CharField(max_length=200,default='')
    follows_me_flag = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.twitter_screen_name + ' at ' + str(self.timestamp)  
    
class Bondee_friends(models.Model):
    bondee = models.ForeignKey(Bondee)
    friend_id_str =  models.CharField(max_length=20,default='')

    def __unicode__(self):
        return self.friend_id_str     