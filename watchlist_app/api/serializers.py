from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Review
        exclude = ('watchlist','review_user') 
        #watchlist는 url로 받기 때문
        #이거 안해주면 watchlist가 필수필드라 에러 뜸
        #('a',) 이 형태는 튜플로 만들어주려고 그러는 거임
        #review_user도 비슷한 맥락. 먼저 is_valid()는 통과시키고려고 이렇게 하는 것
        
        # fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True,read_only=True)
    
    #다음과 같이 이름이 원래 모델명의 foreignkey로 되어있으면, write할때 실패해서 안됨!!1
    # platform = serializers.CharField(source='platform.name',read_only=True)
    
    platform_name = serializers.CharField(source='platform.name',read_only=True)
    
    class Meta:
        model = WatchList
        fields = '__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True)
    #이름이 실제 필드와 연동되어야 한다. watchlists같은 이름을 마음대로 줄 경우, 해당 필드가 무엇을 나타내는지 모름
    #이름을 다르게 줄 경우 source값을 줘야 함
    class Meta:
        model = StreamPlatform
        fields = '__all__'

# def name_length(value):
#     if len(value) < 2 :
#         raise serializers.ValidationError("Name is too short!")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     #수정은 불가. 읽기(직렬화)만 가능
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self,instance,validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
        
#         return instance
    
