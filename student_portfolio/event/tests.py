import http
import json
from django.contrib.auth.models import User, Group
# from django.test import TestCase
from .views import eventApi
# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, RequestsClient, CoreAPIClient

from django.test import Client

# from rest_framework.test import RequestsClient
# factory = APIRequestFactory()
# request = factory.get('/api/event/', {'title': 'new idea'})

# factory = APIRequestFactory()
# user = User.objects.get(username='tuta') #tuta is staff.
#
# view = eventApi
#
# # Make an authenticated request to the view...
# request = factory.get('/api/event/11')
# force_authenticate(request, user=user)
# response = view(request, event_id=11)
# # print(type(response.content))
# # print(type(json.loads(response.content)))
# # print(response.status_code)
# data = json.loads(response.content)
# # print(data.get('id'))
# print(http.HTTPStatus.OK == response.status_code)

#
class EventCRUD(APITestCase):


    def setUp(self):
        # print('in setup')
        staff_group = Group.objects.get_or_create(name='staff')
        student_group = Group.objects.get_or_create(name='student')
        staff_user = User.objects.create(username='tubtab', password='Tubtab12345678')
        student_user_tamtam = User.objects.create(username='tamtam', password='Tamtam12345678')
        student_user_tubtim = User.objects.create(username='tubtim', password='Tubtim12345678')

        staff_group[0].user_set.add(staff_user)
        student_group[0].user_set.add(student_user_tamtam)
        student_group[0].user_set.add(student_user_tubtim)

        # print(group[0])
        #We create read update and delete | We do not have to worry about setting it up and tearing it down.

    def test_staff_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        request = factory.post('/api/event/', {'title': 'โครงการ'} )
        force_authenticate(request, user=user)
        response = view(request, event_id=0)

        response_data = json.loads(response.content)
        # print(response_data)
        data = response_data['data']
        message = response_data['message']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)


    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        # print('event_id : {}'.format(event_id))
        # print(type(event_id))
        # print('/api/event/' + str(event_id))
        request = factory.get('/api/event/' + str(event_id)) #Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        # print(type(response))
        data = json.loads(response.content)
        # print(data)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        #create part
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        self.assertEqual(data['approved'], False)
        out_dict = {'title': 'โครงการ', 'id' : event_id, 'approved': 'true' }

        #Update part
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        # print(type(response))
        response_data = json.loads(response.content)
        # print(response_data)
        data = response_data['data']
        # print(data)
        self.assertEqual(data.get('approved'), True)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        request = factory.delete('/api/event/' + str(event_id))
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['message'], "Deleted Successfully")

    def test_student_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = eventApi

        request = factory.post('/api/event/', {'title': 'Tamtam created โครงการ'})
        force_authenticate(request, user=user)
        response = view(request, event_id=0)

        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['message']

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)

    def test_student_can_read(self):
        # Expect : user can create and read the event created:
        # Expect event id to be the same.
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = eventApi

        # create part
        create_request = factory.post('/api/event/', {'title': 'ฺโครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        self.assertEqual(data['approved'], False)
        out_dict = {'title': 'โครงการ', 'id': event_id, 'approved': 'true'}

        request = factory.get('/api/event/' + str(event_id))  # Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

    def test_student_can_update(self):
        # Case 1 : approved=False : Expect approved to be the same, expect title to change
        # Case 2 : approved=True : Expect : Failed to update.

        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        staff_user = User.objects.get(username='tubtab')  # tuta is staff
        view = eventApi

        # Case 1
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        self.assertEqual(data['title'], 'โครงการ')
        self.assertEqual(data['approved'], False)

        out_dict = {'title': 'changed', 'id': event_id, 'approved': 'true'}

        # Update part
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)
        data = response_data['data']

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

        self.assertEqual(data['title'], 'changed')   # title has changed.
        self.assertEqual(data.get('approved'), False) # approved stays the same, False.

        # Case 2: student cannot update the approved event.
        # staff approves event
        out_dict = {'title': 'changed', 'id': event_id, 'approved': 'true'}
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(data.get('approved'), True)

        #student tries to update the event
        out_dict = {'title': 'changed', 'id': event_id, 'approved': 'true'}
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['message'], "Failed to update.")


    def test_student_can_delete(self):
        # Student can delete the unapproved project created the user.
        # Student cannon deleted approved project nor the project created by other user.


        # event_1 created_by == user.id and approved=False.
        # Expect : The user can delete event_1
        #event_2 created_by user and approved=True.
        # Expect : The user cannot delete event_2
        #event_3 created_by other user.
        # Expect : The user cannot delete event_3

        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tuta is staff.
        student_user_tamtam = User.objects.get(username='tamtam')
        student_user_tubtim = User.objects.get(username='tubtab')
        view = eventApi

        # Expect : The user can delete event_1
        # event_1 created_by == user.id and approved=False.
        #create event_1
        create_request = factory.post('/api/event/', {'title': 'event 1'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_1_id = data.get('id')
        #delete event_1
        request = factory.delete('/api/event/' + str(event_1_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=event_1_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['message'], "Deleted Successfully")


        # event_2 created_by user and approved=True.
        # Expect : The user failed delete event_2.

        # create event_2
        create_request = factory.post('/api/event/', {'title': 'event 2'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_2_id = data.get('id')

        #staff approves event_2
        out_dict = {'title': 'changed', 'id': event_2_id, 'approved': 'true'}
        request = factory.put('/api/event/' + str(event_2_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, event_id=event_2_id)
        response_data = json.loads(response.content)
        data = response_data['data']

        # An attempt to delete event_2. (tamtam tries to delete event_2.)
        request = factory.delete('/api/event/' + str(event_2_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=event_2_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['message'], "Failed to delete.")

        # event_3 created_by other user.
        # Expect : The user cannot delete event_3
        # Note : created_by tubtim but tamtam tries to delete the event.
        #create event_3 (by tubtim)
        create_request = factory.post('/api/event/', {'title': 'event 3'})
        force_authenticate(create_request, user=student_user_tubtim)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_3_id = data.get('id')

        # An attempt to delete event_3. (tamtam tries to delete event_3)
        request = factory.delete('/api/event/' + str(event_3_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=event_3_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['message'], "Failed to delete.")

    def test_unauthenticated_create(self):

        # expect Forbidden

        factory = APIRequestFactory()
        request = factory.post('/api/event/', {'title': 'event 2'})
        request = factory.get('/api/event/')
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=0)

        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_read(self):
        # expect Forbidden

        factory = APIRequestFactory()
        request = factory.get('/api/event/')
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=0)

        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_update(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        # create part
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id', None)
        self.assertNotEqual(event_id, None)

        #the unauthenticated user tries to update the project
        request = factory.put('/api/event/' + str(event_id), {'title': 'โครงการที่ถูกแก้ไข'})
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=event_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_delete(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        # create part
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id', None)
        self.assertNotEqual(event_id, None)

        #the unauthenticated user tries to update the project
        request = factory.delete('/api/event/' + str(event_id))
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=event_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)