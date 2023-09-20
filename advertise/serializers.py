from rest_framework import serializers

from advertise.models import Advertise, AdvertiseImage
from account.serializers import UserSerializer


class AdvertiseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiseImage
        fields = ['id', 'advertise_id', 'image']


class AdvertiseListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    def get_image(self, obj):
        try:
            ad_image: AdvertiseImage = obj.images.first()
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(ad_image.image.url)
            return AdvertiseImageSerializer(instance=ad_image).data
        except AttributeError:
            return None

    class Meta:
        model = Advertise
        fields = ['id', 'user', 'title', 'price', 'created', 'image']
