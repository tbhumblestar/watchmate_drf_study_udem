from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

import json


class RegisterTestCase(APITestCase):
    
    #test로 시작되지 않으면 실행되지 않음
    def test_register(self):
        data = {
            'username':'testcase',
            'email':'testcase@example.com',
            'password': 'p9l9o9k9!2',
            'password2' : 'p9l9o9k9!2'
        }
        
        #reverse : url이름을 찍어주면 알아서 endpoint를 잡아줌
        #post > url , data, 
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
class LoginLogoutTestCase(APITestCase):
    
    #데이터를 생성
    def setUp(self):
        self.user = User.objects.create_user(
            username='testcase',
            # email='testcase@example.com',
            password='p9l9o9k9!2',
            # password2='p9l9o9k9!2'
            )
        
    def test_login(self):
        data = {
    "username":"testcase",
    "password":"p9l9o9k9!2"
}
        
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_logout(self):
        #token을 받아와야 함
        self.token = Token.objects.get(user__username='testcase')
        
        #client에 credentials를 부여
        #header의 Authorization에 Token을 담음
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        
        response = self.client.post(reverse('logout'))
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)