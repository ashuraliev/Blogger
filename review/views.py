from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, LikeComment
from .serializers import CommentSerializer

User = get_user_model()

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # если detail=True в url добавляется id
    @action(['POST'], detail=False)
    def like(self, request):
        author_id = request.data.get("author")
        comment_id = request.data.get("comment")
        author = get_list_or_404(User, id=author_id)
        comment = get_list_or_404(Comment, id=comment_id)

        if LikeComment.objects.filter(author=author, comment=comment).exists():
            # если лайк есть
            LikeComment.objects.filter(author=author, comment=comment).delete()
            # удаляем
        else:
            LikeComment.objects.create(author=author, comment=comment)
        return Response(status=201)