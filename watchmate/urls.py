from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist_app.api.urls')),
    path('account/', include('user_app.api.urls')),
    
    #JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #drf의 login api임. 여기로 api를 보내면 로그인/로그아웃해줌
    # path('api-auth/', include('rest_framework.urls')),
]
