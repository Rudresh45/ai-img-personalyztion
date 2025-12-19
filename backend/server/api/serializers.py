from rest_framework import serializers
from .models import PersonalizationRequest


class PersonalizationRequestSerializer(serializers.ModelSerializer):
    """Serializer for PersonalizationRequest model"""
    
    class Meta:
        model = PersonalizationRequest
        fields = [
            'id',
            'uploaded_photo',
            'illustration',
            'result_image',
            'status',
            'created_at',
            'updated_at',
            'error_message',
            'face_confidence'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status', 'result_image', 'error_message', 'face_confidence']


class UploadSerializer(serializers.Serializer):
    """Serializer for initial photo upload"""
    
    uploaded_photo = serializers.ImageField(required=True)
    illustration = serializers.ImageField(required=False, allow_null=True)
    
    def validate_uploaded_photo(self, value):
        """Validate uploaded photo"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Photo file size must be less than 10MB")
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG and PNG images are allowed")
        
        return value
    
    def validate_illustration(self, value):
        """Validate illustration if provided"""
        if value:
            # Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Illustration file size must be less than 10MB")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG and PNG images are allowed")
        
        return value
