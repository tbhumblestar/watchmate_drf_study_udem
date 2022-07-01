from django.urls import path,include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import WatchDetailAV,WatchListAV,StreamPlatformListAV,StreamPlatformDetailAV,ReviewList,ReviewDetail,ReviewCreate, StreamPlatformVS, UserReview, WatchListAV2

router = DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')

urlpatterns = [
    path('list/',WatchListAV.as_view(),name='watch-list'),
    path('list2/',WatchListAV2.as_view(),name='watch-list2'),
    path('<int:pk>/',WatchDetailAV.as_view(),name='watch-detail'),
    
    #router
    path('',include(router.urls)),
    # path('stream/',StreamPlatformListAV.as_view(),name='stream-list'),
    # path('stream/<int:pk>',StreamPlatformDetailAV.as_view(),name='stream-detail'),
    
    
    
    path('<int:pk>/reviews/',ReviewList.as_view(),name='review-list'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    #filter : url_kwarg
    path('review/<str:username>/',UserReview.as_view(),name='userreview-detail'),
    #filter : query_param
    # path('stream/review/',UserReview.as_view(),name='userreview-detail'),
    # path('review',ReviewList.as_view(),name='review-detail'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),
]

