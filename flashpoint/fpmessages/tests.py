from django.test import TestCase
from fpmessages.models import *
import datetime

class MessageMethodsTestCase(TestCase):
  def setUp(self):
    location = Location(city="Albuquerque", 
                        state="New Mexico")
    location.save()

    user = User(name="Dave",
                location=location)
    user.save()

    message = Messages(user=user, 
                       message="hello!", 
                       create_time=datetime.datetime.now())
    message.save()

  def test_counts(self):
    self.assertEqual(Messages.objects.all().count(),1)
    self.assertEqual(User.objects.all().count(),1)
    self.assertEqual(Location.objects.all().count(),1)
  def test_city_property(self):
    m = Messages.objects.all()[0]
    self.assertEqual(m.city, 'Albuquerque')

  def test_state_propery(self):
    m = Messages.objects.all()[0]
    self.assertEqual(m.state, 'New Mexico')
  
  def test_username_propery(self):
    m = Messages.objects.all()[0]
    self.assertEqual(m.username, 'Dave')
