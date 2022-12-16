from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from review.models import LikePost

from .models import Post
from .serializers import PostSerializer


User = get_user_model()

@api_view(['GET'])
def post_list(request):
    queryset = Post.objects.all().order_by('id')
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=201)

@api_view(['PATCH'])
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=201)    

@api_view(['DELETE'])
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post:
        post.delete()
        return Response(status=201)

@api_view(['GET'])
def filter_by_user(request, u_id):
    author = get_object_or_404(User, id=u_id)
    queryset = Post.objects.filter(author__id=u_id)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def search(request):
    q = request.query_params.get('q')
    queryset = Post.objects.filter(body__icontains=q)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def toggle_like(request):
    post_id = request.data.get("post")
    author_id = request.data.get("author")
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, id=author_id)

    if LikePost.objects.filter(post=post, author=author).exists():
        # если был лайк
        LikePost.objects.filter(post=post, author=author).delete()
        # удаляем
    else:
        # если лайка нет
        LikePost.objects.create(post=post, author=author)
        # создаем
    return Response(status=201)


from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
# from rest_framework.serializers import UserSerializer


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer
from .models import User
from .serializers import UserSerializer


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Вы успешно зарегистрировались", status=201)

class DeleteUserView(APIView):
    def delete(self, request,email):
        user = get_object_or_404(User, email=email)
        print(user)
        print(request.user)
        if user.is_staff or user != request.user:
            return Response(status=403)
        user.delete()
        return Response(status=204) 

class UserListView(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer