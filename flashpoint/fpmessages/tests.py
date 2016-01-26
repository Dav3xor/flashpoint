from django.test       import TestCase
from fpmessages.models import *
from fpmessages.views  import *

import datetime, random

first_names = ['David','Jim','Laura','Jeff','Cecilia','Anna','Shaun','Matt','George']
last_names  = ['Smith','Jones','Sanchez','Baker','Miller','Winters','Bishop']

cities      = ['Portland', 'New York', 'San Francisco', 'Austin']
states      = ['Oregon', 'New York', 'California', 'Texas']

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

class CountersTestCase(TestCase):
  def test_counters(self):
    Counters.increment('test')
    self.assertEqual(Counters.objects.get(key='test').value, 1)
    Counters.decrement('test')
    self.assertEqual(Counters.objects.get(key='test').value, 0)
    self.assertEqual(Counters.current_value('test'), 0)
    
class StatsViewTestCase(TestCase):
  def setUp(self):
    random.seed(0)
    for i in xrange(1000):
      username = random.choice(first_names) + " " + random.choice(last_names)
      city     = random.choice(cities)
      state    = random.choice(states)

      location = Locations.objects.get_or_create(city=city,state=state)[0]
      user     = Users.objects.get_or_create(name=username,location=location)[0]
      message  = Messages.objects.get_or_create(user=user, message="message #" + str(i))
  
  def test_num_messages(self):
    self.assertEqual(Messages.objects.count(),1000)

  def test_num_users(self):
    self.assertEqual(Users.fast_count(),637)

  def test_num_locations(self):
    self.assertEqual(Locations.fast_count(),16)
  
  def test_stats_view(self):
    response = stats('request')
    self.assertEqual(response.serialize(),
                     'Content-Type: application/json\r\n\r\n{"cities": 16, "users": 637, "result": "success"}')

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
