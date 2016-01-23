from __future__ import unicode_literals
from django.db import models



class Location(models.Model):
  state        = models.CharField('State', max_length=64)
  city         = models.CharField('City', max_length=64)
 
class User(models.Model):
  name         = models.CharField('User', max_length=64)
 
class Messages(models.Model):
  username     = models.CharField('User', max_length=64)
  message      = models.TextField('Message')
  create_time  = models.DateTimeField('Date', auto_now_add=True)

  # make properties for fields in original specification
  # that are now parts of different tables.
  @property
  def username(self):
    return self.user.name

  @property
  def state(self):
    return self.user.location.state

  @property
  def city(self):
    return self.user.location.city

  class Meta:
    ordering = ['user__location__state', 'user__location__city', 'create_time']
