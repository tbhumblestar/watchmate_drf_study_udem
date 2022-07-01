
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#참고 : https://docs.djangoproject.com/en/4.0/ref/signals/


#recevier : 신호를 받으면 작동함 > 얘가 작동하려면, 신호를 보내는 곳에 import 되어 있거나 신호보내는 파일에 있어야 함
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    #sender : 신호를 보낸 모델클래스
    #instance : 현재 기능이 수행된 모델의 인스턴스
    #created : 새 데이터가(레코드) 생성될 경우 True. 즉 업데이트 되는 save일 경우 False임
    if created:
        Token.objects.create(user=instance)