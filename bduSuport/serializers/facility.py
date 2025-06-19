"""Facility serializer for API operations."""

from rest_framework import serializers
from bduSuport.models.facility import Facility
from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider


class FacilitySerializer(serializers.ModelSerializer):
    """Serializer for Facility model."""
    
    class Meta:
        model = Facility
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    
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
    description = serializers.CharField(required=True)
    image = serializers.FileField(required=True)
    
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
        image_file = validated_data.pop('image')
        storage_provider = FirebaseStorageProvider()
        image_url = storage_provider.upload_file(image_file)
        
        facility = Facility.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            image_url=image_url
        )
        return facility


class FacilityUpdateSerializer(serializers.Serializer):
    """Serializer for updating existing facilities."""
    
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    image = serializers.FileField(required=False)
    
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
        
        if 'image' in validated_data:
            storage_provider = FirebaseStorageProvider()
            image_url = storage_provider.upload_file(validated_data['image'])
            instance.image_url = image_url
        
        instance.save()
        return instance 