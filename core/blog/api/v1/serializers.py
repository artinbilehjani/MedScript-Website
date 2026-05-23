from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name", "id"]


class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField()
    snippet = serializers.ReadOnlyField(source="get_snippets")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "image",
            "author",
            "content",
            "snippet",
            "absolute_url",
            "published_date",
            "created_date",
            "status",
            "category",
            "relative_url",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_api_url())

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        rep["sate"] = "list"
        if request.parser_context.get("kwargs").get("pk"):
            rep["sate"] = "single"
            rep.pop("snippet")
            rep.pop("relative_url")
            rep.pop("absolute_url")
        else:
            rep.pop("content")
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
