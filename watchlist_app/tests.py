from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models
import json

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example',password='p9l9o9k9!2')
        self.token = Token.objects.get(user__username=self.user.username)
        
        #token인증을 위해 달아줌
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
        self.stream = models.StreamPlatform.objects.create(
            name = "Netflix",
            about = "#1 Streaming PlatForm",
            website = "https://netflix.com"
        )
    
    def test_streamplatform_create(self):
        data = {
            "name":"Netflix",
            "about":"#1 Streaming PlatForm",
            "website":"https://netflix.com"
        }
        
        #router를 사용시, 자동으로 name이 패턴에 맞게 생성됨. 아래 참고
        #https://www.django-rest-framework.org/api-guide/routers/
        response = self.client.post(reverse('streamplatform-list'),data)
        
        #관리자만 할 수 있음
        #일반사용자라 인증은되어서 401은 안뜨는데, 금지되어 있어서 403이뜸
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        
        #이렇게 주면 url관련 url_kwarg를 줄 수 있음
        #url_kwarg는 여러개 일 수 있으니 튜플로 줌
        response = self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # self.assertEqual(response.json(),status.HTTP_200_OK)
        

class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example',password='p9l9o9k9!2')
        self.token = Token.objects.get(user__username=self.user.username)
        
        #token인증을 위해 달아줌
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
        self.stream = models.StreamPlatform.objects.create(
            name = "Netflix",
            about = "#1 Streaming PlatForm",
            website = "https://netflix.com"
        )
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title = 'Example title',
            storyline = 'Example Story',
            active = True
        )
        
    def test_watchlist_create(self):
        data = {
            'platform':self.stream.id,
            'title':'Example Movie',
            'storyline':'Example Story',
            'active':True
        }
        
        #super_user만 가능하므로 ㅇㅇ
        response = self.client.post(reverse('watch-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('watch-detail',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        #모델에 데이터가 하나이면, get으로 조회시 한개의 데이터가 바로 선택됨
        self.assertEqual(models.WatchList.objects.get().title,'Example title')
        
        self.assertEqual(models.WatchList.objects.count(),1)