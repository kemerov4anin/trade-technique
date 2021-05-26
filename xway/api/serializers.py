from rest_framework import serializers
from .models import Albums, Photos


class PhotosSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "%s > %s > %s > %s > %s" % (
            value.id,
            value.title,
            value.url,
            value.thumbnailUrl,
            value.localUrl
        )

    class Meta:
        model = Photos
        fields = ('id', 'localUrl',)


class AlbumsSerializer(serializers.ModelSerializer):
    photos = PhotosSerializer(many=True, read_only=True)

    class Meta:
        model = Albums
        fields = ('id', 'title', 'userId', 'photos')
        read_only_fields = ('photos',)


