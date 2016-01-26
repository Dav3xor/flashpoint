from __future__ import unicode_literals
from django.db import models

class Counters(models.Model):
  # obvious optimization: use something faster than a SQL
  # database to store these key-value pairs.  Redis would
  # be good for this...
  """A Django model for storing a counter under a key. """
  key          = models.CharField('Key', max_length=64)
  value        = models.PositiveIntegerField('Value', default=0)

  # I could make these class methods, but it would mostly
  # just be extra typing...
  @classmethod
  def get_counter(cobj, key):
    counter = cobj.objects.get_or_create(key=key)[0]
    return counter

  @classmethod
  def increment(cobj, key):
    counter = cobj.get_counter(key)
    counter.value += 1
    counter.save()

  @classmethod
  def decrement(cobj, key):
    # this isn't terribly DRY, but for brevity's sake.
    counter, isnew = cobj.objects.get_or_create(key=key)
    counter.value -= 1
    counter.save()

  @classmethod
  def current_value(cobj, key):
    counter, isnew = cobj.objects.get_or_create(key=key)
    return counter.value


# Abstract class gives quick countability to derived Models

# this system only works if you only access these tables
# through the django models.  if you add/delete a record
# outside of Django, it will lose sync.
class Countable(models.Model):
  """An abstract class to make a Django Model fast-countable"""
  def save(self, *args, **kwargs):
    Counters.increment("num_"+self._meta.db_table+"_objects")
    return super(Countable, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    # see comment about DRY above.
    Counters.decrement("num_"+self._meta.db_table+"_objects")
    return super(Countable, self).delete(*args, **kwargs)

  @classmethod
  def fast_count(counter_obj):
    return Counters.current_value("num_"+counter_obj._meta.db_table+"_objects")

  class Meta:
    abstract=True

  
# store each state/city pair as a location.  There
# can be more than one city with the same name in
# different states.  Portland Maine, Portland Oregon,
# etc.
class Locations(Countable):
  """Django Model for storing city/state pairs"""
  state        = models.CharField('State', max_length=64)
  city         = models.CharField('City', max_length=64)


# also store the users in a separate table
class Users(Countable):
  """
  Django Model for storing users for Messages, I should have
  probably used the normal Django User, but did this for...  
  (once again) brevity.
  """
  name         = models.CharField('User', max_length=64)
  location     = models.ForeignKey('Locations')
  class Meta:
    unique_together = ('name','location')
   
class Messages(models.Model):
  # I'm making an assumption that a user has a permanently
  # set location; if the location is meant to be for where the
  # user is sending the message from, put a foreign key to
  # location here
  """Django Model for storing messages for users"""
  user         = models.ForeignKey('Users')
  message      = models.TextField('Message')
  create_time  = models.DateTimeField('Date', auto_now_add=True)

  # make properties for fields in original specification
  # that are now parts of different tables.  Leaving
  # out setters for brevity.
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
