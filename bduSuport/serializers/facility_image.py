from rest_framework import serializers
from bduSuport.models.facility_image import FacilityImage
from bduSuport.models.facility import Facility
from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider


class FacilityImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FacilityImage
        fields = "__all__"

class FacilityImageCreateSerializer(serializers.Serializer):
    facility = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.filter(deleted_at=None)
    )
    image = serializers.FileField(required=True)
    
    def create(self, validated_data):
        image_file = validated_data.pop('image')
        storage_provider = FirebaseStorageProvider()
        image_url = storage_provider.upload_file(image_file)
        
        facility_image = FacilityImage.objects.create(
            facility=validated_data['facility'],
            image_url=image_url
        )
        return facility_image 