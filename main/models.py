from django.db import models


class Tweet(models.Model):
    tweet_text = models.CharField(max_length=255, null=True, blank=True)
    time_stamp = models.CharField(max_length=255, null=True, blank=True)
    screen_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    search_term = models.CharField(max_length=255, null=True, blank=True)
    time_handle = models.CharField(max_length=255, null=True, blank=True)

    profile_image_url = models.ImageField(upload_to="profile_images",
                                          null=True,
                                          blank=True)

    def __unicode__(self):
        return self.tweet_text
