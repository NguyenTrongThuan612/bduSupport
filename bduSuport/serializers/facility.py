from rest_framework import serializers
from bduSuport.models.facility import Facility
from bduSuport.serializers.facility_image import FacilityImageSerializer


class FacilitySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = "__all__"
    
    def get_images(self, obj):
        active_images = obj.images.filter(deleted_at=None)
        return FacilityImageSerializer(active_images, many=True).data
    
    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)
    
    def validate_name(self, value):
        """Validate facility name."""
        if not value or not value.strip():
            raise serializers.ValidationError("Facility name cannot be empty")
        return value.strip()
    
    def validate_description(self, value):
        """Validate facility description."""
        if not value or not value.strip():
            raise serializers.ValidationError("Facility description cannot be empty")
        return value.strip()


class FacilityCreateSerializer(serializers.Serializer):
    """Serializer for creating new facilities."""
    
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    
    def validate_name(self, value):
        """Validate facility name."""
        if not value or not value.strip():
            raise serializers.ValidationError("Facility name cannot be empty")
        return value.strip()
    
    def validate_description(self, value):
        """Validate facility description."""
        if not value or not value.strip():
            raise serializers.ValidationError("Facility description cannot be empty")
        return value.strip()
    
    def create(self, validated_data):
        """Create and return a new Facility instance."""
        facility = Facility.objects.create(
            name=validated_data['name'],
            description=validated_data['description']
        )
        return facility


class FacilityUpdateSerializer(serializers.Serializer):
    """Serializer for updating existing facilities."""
    
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    
    def validate_name(self, value):
        """Validate facility name."""
        if value and not value.strip():
            raise serializers.ValidationError("Facility name cannot be empty")
        return value.strip() if value else value
    
    def validate_description(self, value):
        """Validate facility description."""
        if value and not value.strip():
            raise serializers.ValidationError("Facility description cannot be empty")
        return value.strip() if value else value
    
    def update(self, instance, validated_data):
        """Update and return an existing Facility instance."""
        if 'name' in validated_data:
            instance.name = validated_data['name']
        
        if 'description' in validated_data:
            instance.description = validated_data['description']
        
        instance.save()
        return instance 