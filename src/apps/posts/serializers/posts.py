from typing import TypeVar

from rest_framework import serializers

from apps.profiles.services import get_profile

from ..models import Post, PostMedia

PostSerializeT = TypeVar("PostSerializeT", bound=serializers.ModelSerializer)


class PostMediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("description", "medias", "is_active", "creator")

    def create(self, validated_data):
        validated_data["creator"] = get_profile(user=self.context.get("request").user)
        result = super().create(validated_data)
        return result


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "medias")
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        depth = 1


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("creator", "medias")
