from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.models import WatchList,StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from watchlist_app.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

#throttling
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle

#filtering(56강)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

#pagination
from watchlist_app.api.pagination import WatchListPagination,WatchListLOPPagination, WatchListCPagination

#filter(55강)
class UserReview(generics.ListAPIView):
    
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    
    
    # #이게 없으면, 어떤 경우에나 모든 영화리스트를 가져옴
    # def get_queryset(self):
    #     username = self.kwargs['username']#urls.py 로부터 얻음
    #     return Review.objects.filter(review_user__username=username)
    
    def get_queryset(self):
        #url_kwargs 쓰는 경우
        # username = self.kwargs['username']
        #query_params를 쓰는 경우
        username = self.request.query_params.get('username',None)
        
        print("\n")
        print("print_test_in_testing")
        print("\n")

        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    # throttle_classes = [ReviewCreateThrottle]
    permission_classes =[IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        #perform_create를 호출하는 create가 kwargs를 받음(url)
        # 그래서 self.kwargs.get('pk')로 pk에 접근이 가능하다.
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        
        if Review.objects.filter(watchlist=watchlist,review_user=review_user).exists():
            raise ValidationError("You have already reviewd the watchlist")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']/2)
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
            
        
        #serializer(request.data)
        #serializer.is_valid()는 이미 다른 곳에서 진행되어 있음
        #serializer.save()만해주면 됨
        
        serializer.save(watchlist=watchlist,review_user=review_user)
        
#ListCreate > List (Create삭제)
class ReviewList(generics.ListAPIView):
    
    # permission_classes = (IsAuthenticated,)
    # throttle_classes = [UserRateThrottle,AnonRateThrottle]
    #filter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    #이게 없으면, 어떤 경우에나 모든 영화리스트를 가져옴
    def get_queryset(self):
        pk = self.kwargs['pk']#urls.py 로부터 얻음
        return Review.objects.filter(watchlist=pk)



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsReviewUserOrReadOnly,)

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# #Streat : ViewSet
# class StreamPlatformVS(viewsets.ViewSet):
#     """
#     This viewset automatically provides `list` and `retrieve` actions.
#     """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer 
    permission_classes = [IsAdminOrReadOnly]


class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        platform =  StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(streamplatform,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(streamplatform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
        streamplatform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class WatchListAV2(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    

class WatchDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self,request,pk):
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                            
                            
        


################################################################
# FBV

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         #쿼리 개수가 많음 > many=True
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT','DELETE'])
# def movie_details(request,pk):
    
#     try:
#         movie = Movie.objects.get(id=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error":"Movie not found"},status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         serializer = MovieSerializer(movie,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=204)
        

################################################################
# example 1

# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse

# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {'movies':list(movies.values())}
#     return JsonResponse(data)
    
# def movie_details(request,pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         'name':movie.name,
#         'description':movie.description,
#         'active':movie.active
#     }
#     return JsonResponse(data)