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
        
class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example',password='p9l9o9k9!2')
        self.token = Token.objects.get(user__username=self.user.username)
        
        #token인증을 위해 달아줌
        #이렇게 해주면 client를 통해 요청을 보낼 때 authorization에 token을 넣어줄 수 있음
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
        
        
        #WatchList2를 만든 이유
        #유저는 watchlist하나당 한개의 리뷰만 쓸 수 있다보니, watchlist가 하나이면 test하면서 무조건 에러가 남
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,
            title = 'Example title',
            storyline = 'Example Story',
            active = True
        )
        self.review = models.Review.objects.create(
            review_user = self.user,
            rating = 5,
            description = "reviews",
            watchlist = self.watchlist2,
            active = True
        )
    def test_review_create(self):
        data = {
            'review_user':self.user,
            'rating':5,
            'description':'Great Moview!',
            'watchlist':self.watchlist,
            'active':True            
        }
        
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        #유저하나당 리뷰는 하나이므로, 똑같은 리뷰생성요처을 두번보내면 400이 와야 함
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        #모델에 데이터가 하나이면, get으로 조회시 한개의 데이터가 바로 선택됨
        #근데 review를 하나 더 만들어주면서 사용하지 못함 > 이런방식은 애초에 좋지 않음
        # self.assertEqual(models.Review.objects.get().rating,5)
        
        #
        self.assertEqual(models.Review.objects.filter(watchlist=self.watchlist).get().rating,5)
        
        self.assertEqual(models.Review.objects.count(),2)
        
    #인증되지 않은 유저의 리뷰 생성 테스트 > 인증이 안되어 있으므로 401이 와야 함
    def test_review_create_unauth(self):
        data = {
            'review_user':self.user,
            'rating':5,
            'description':'Great Moview!',
            'watchlist':self.watchlist,
            'active':True            
        }
        
        #인증된 유저가 없게(None) 함
        #강제로 특정 유저의 인증가 인증되도록 하게 하려면 self.client.force_authenticate(user=user)
        #참고 : https://www.django-rest-framework.org/api-guide/testing/#authenticating
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data = {
            'review_user':self.user,
            'rating':5,
            'description':'Great Moview!-updated!',
            'watchlist':self.watchlist,
            'active':False   
        }
        
        response = self.client.put(reverse('review-detail',args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    #detail
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_user(self):
        
        #쿼리파라미터때문에 reverse를 못쓴다!
        response = self.client.get('/watch/review/?username='+self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('id'),1)