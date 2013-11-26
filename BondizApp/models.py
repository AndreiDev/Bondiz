from django.db import models
from django.core.validators import RegexValidator

class Bondi(models.Model):
    twitter_screen_name = models.CharField(max_length=20,default='')
    
    email = models.CharField(max_length=40,default='')
    plan = models.IntegerField(default=1)
    notification_timestamp = models.CharField(max_length=10,default='')
    active_flag = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.twitter_screen_name
    
class List(models.Model):
    bondi = models.ForeignKey(Bondi)
    list_name = models.CharField(max_length=30,default='')
    active_flag = models.BooleanField(default=True)

    realtime_keywords_RT_flag = models.BooleanField(default=True)
    realtime_keywords_FAV_flag = models.BooleanField(default=True)
    realtime_popular_RT_flag = models.BooleanField(default=True)
    realtime_popular_FAV_flag = models.BooleanField(default=True)
    realtime_popular_time_period = models.IntegerField(default=2)
    realtime_popular_RT_threshold = models.IntegerField(default=2)
    realtime_popular_FAV_threshold = models.IntegerField(default=2)
    
    report_friends_num = models.IntegerField(default=2)
    report_follows_me_flag = models.BooleanField(default=True)
    report_change_bio_flag = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.list_name  
    
class Tweet_keyword(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    bondi_list = models.ForeignKey(List)
    keyword = models.CharField(max_length=20,default='', validators=[alphanumeric])
    
    def __unicode__(self):
        return self.keyword  
    
class Bondee(models.Model):
    bondi = models.ForeignKey(Bondi)
    twitter_screen_name = models.CharField(max_length=20,default='')
    
    followers_num = models.IntegerField(default=0)
    friends_num = models.IntegerField(default=0)
    profile_bio = models.CharField(max_length=200,default='')
    follows_me_flag = models.BooleanField(default=True)

    def __unicode__(self):
        return self.twitter_screen_name 
    
class Log(models.Model):
    bondi = models.ForeignKey(Bondi)
    message = models.CharField(max_length=1000,default='')
    message_timestamp = models.CharField(max_length=10,default='')

    def __unicode__(self):
        return self.message     