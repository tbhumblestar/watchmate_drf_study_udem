from rest_framework.decorators        import api_view
from rest_framework.response          import Response
from rest_framework.authtoken.models  import Token
from rest_framework  import status
from user_app.api.serializers         import RegistrationSerializer
from user_app                         import models

#JWT
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save() #post_save신호가 감
            
            data['response'] = 'Registration Success!'
            data['username'] = account.username
            data['email']    = account.email
            
            token = Token.objects.get(user=account).key
            data['token'] = token
            
            #jwt
    #         refresh = RefreshToken.for_user(account)
    #         data['jwt'] = {
    #             'refresh': str(refresh),
    #             'access': str(refresh.access_token),
    # }
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors            
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)