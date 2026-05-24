from rest_framework import serializers
from ...models import Post, Category,Tag
from accounts.models import Profile
from rest_framework.parsers import JSONParser


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name", "id"]

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["name", "id"]

class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField()
    snippet = serializers.ReadOnlyField(source="get_snippets")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")
    hit_count = serializers.SerializerMethodField(method_name="get_hit_count")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "author",
            "content",
            'links',
            "snippet",
            "absolute_url",
            "relative_url",
            "published_date",
            "created_date",
            "status",
            "category",
            "tag",
            "hit_count",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.get_absolute_api_url())
        return obj.get_absolute_api_url()

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        rep["state"] = "list"

        if request and request.parser_context.get("kwargs", {}).get("pk"):
            rep["state"] = "single"
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)

        rep["category"] = CategorySerializer(
            instance.category.all(),
            context={"request": request},
            many=True,
        ).data
        rep["tag"] = TagSerializer(
            instance.tag.all(),
            context={"request": request},
            many=True,
        ).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def get_hit_count(self, obj):
        hit_count_obj = obj.hit_count_generic.all().first()
        return hit_count_obj.hits if hit_count_obj else 0
        
