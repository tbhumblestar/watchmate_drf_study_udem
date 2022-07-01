from django.contrib.auth.models import User
from rest_framework import serializers
from user_app.models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model = User
        #username, email, p1,p2등의 속성이 이미 있음
        fields = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
            #password를 쓸 수만 있게. 읽을 수는 없음
        }
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        #같은지 비교하는 작업. 직접해줘야 함
        
        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be same'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})
        
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account