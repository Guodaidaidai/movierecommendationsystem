# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse



class MovieInfo(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=100)
    m_type = models.CharField(max_length=100, blank=True, null=True)
    m_country = models.CharField(max_length=50, blank=True, null=True)
    m_year = models.CharField(max_length=100, blank=True, null=True)
    post_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_info'

    def __str__(self):
        return str(self.m_id)

    def get_absolute_url(self):
        return reverse('comment:movie_info',args=[self.m_id])




class Sentimentclassify(models.Model):
    m = models.ForeignKey(MovieInfo, models.DO_NOTHING)
    index = models.AutoField(primary_key=True)
    bad_count = models.IntegerField(blank=True, null=True)
    middle_count = models.IntegerField(blank=True, null=True)
    good_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentimentClassify'

    def __str__(self):
        return str(self.m)

    def get_absolute_url(self):
        return reverse('comment:sentiment_classify',args=[self.m])


class ShortComments(models.Model):
    c_id = models.AutoField(primary_key=True)
    m = models.ForeignKey(MovieInfo, models.DO_NOTHING, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    vote_num = models.CharField(max_length=10, blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)
    u = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)
    sentiment = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'short_comments'

    def __str__(self):
        return str(self.c_id)


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=50, blank=True, null=True)
    u_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return str(self.u_id)

class MovieRating(models.Model):
    m_id = models.AutoField(primary_key=True)
    rating = models.FloatField(null=False)

    class Meta:
        managed = False
        db_table = 'movie_rating'

    def __str__(self):
        return str(self.m_id)


