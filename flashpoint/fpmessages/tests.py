from django.test       import TestCase
from fpmessages.models import *
from fpmessages.views  import *
import datetime

class ViewDecoratorsTestCase(TestCase):
  def test_return_json(self):
    @return_json
    def success(request):
      return {'test': True}

    @return_json
    def failure(request):
      5/0 # throw an exception
      return {'test': True}

    self.assertEqual(success('bogus').content,
                     '{"test": true, "result": "success"}')
    self.assertEqual(failure('bogus').content,
                     '{"result": "error", "error": "integer division or modulo by zero"}')

class MessageMethodsTestCase(TestCase):
  def setUp(self):
    location = Locations(city="Albuquerque", 
                        state="New Mexico")
    location.save()

    user = Users(name="Dave",
                location=location)
    user.save()

    message = Messages(user=user, 
                       message="hello!", 
                       create_time=datetime.datetime.now())
    message.save()

  def test_counts(self):
    self.assertEqual(Messages.objects.all().count(),1)
    self.assertEqual(Users.objects.all().count(),1)
    self.assertEqual(Locations.objects.all().count(),1)
  def test_city_property(self):
    m = Messages.objects.all()[0]
    self.assertEqual(m.city, 'Albuquerque')

  def test_state_propery(self):
    m = Messages.objects.all()[0]
    self.assertEqual(m.state, 'New Mexico')
  
  def test_username_propery(self):
    m = Messages.objects.all()[0]
    self.assertEqual(m.username, 'Dave')
