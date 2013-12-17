from django.db import models

class Stalk_task(models.Model):
    target_username     = models.CharField(max_length=20,default='')
    email               = models.CharField(max_length=40,default='')  
    created_at          = models.DateTimeField()
    tweet_id            = models.CharField(max_length=20,default='')
    tweet_text          = models.CharField(max_length=150,default='')    
    sent_flag           = models.BooleanField(default=False)
        
    def __unicode__(self):
        return self.target_username