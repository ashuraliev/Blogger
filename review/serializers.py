from rest_framework.serializers import ModelSerializer
from .models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = instance.author.username
        del rep['post']
        rep['likes'] = instance.likes.count()
        return rep