from rest_framework.serializers import ModelSerializer
from .models import Post
from review.serializers import CommentSerializer


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance:Post):
        rep =  super().to_representation(instance)
        rep["author"] = instance.author.username
        comments = instance.comments.all()
        rep['comments'] = CommentSerializer(comments, many=True).data
        rep['likes'] = instance.likes.count()
        return rep