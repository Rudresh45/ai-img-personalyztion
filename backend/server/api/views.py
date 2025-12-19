from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.conf import settings
import os
import threading

from .models import PersonalizationRequest
from .serializers import PersonalizationRequestSerializer, UploadSerializer
from .ai_service import AIPersonalizationService


@api_view(['POST'])
def upload_photo(request):
    """
    Upload a child's photo and optionally an illustration
    
    POST /api/upload/
    Body: multipart/form-data
        - uploaded_photo: image file (required)
        - illustration: image file (optional)
    
    Returns:
        - 201: Created with request ID
        - 400: Validation error
    """
    serializer = UploadSerializer(data=request.data)
    
    if serializer.is_valid():
        # Create personalization request
        personalization_request = PersonalizationRequest.objects.create(
            uploaded_photo=serializer.validated_data['uploaded_photo'],
            illustration=serializer.validated_data.get('illustration'),
            status='pending'
        )
        
        response_serializer = PersonalizationRequestSerializer(personalization_request)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def process_in_background(request_id):
    """Background task to process personalization"""
    try:
        # Get the request
        personalization_request = PersonalizationRequest.objects.get(id=request_id)
        personalization_request.status = 'processing'
        personalization_request.save()
        
        # Initialize AI service
        ai_service = AIPersonalizationService()
        
        # Get file paths
        photo_path = personalization_request.uploaded_photo.path
        
        # Use provided illustration or default
        if personalization_request.illustration:
            illustration_path = personalization_request.illustration.path
        else:
            # Use a default illustration (you'll need to provide one)
            illustration_path = os.path.join(settings.MEDIA_ROOT, 'default_illustration.png')
            
            # If no default exists, create a simple placeholder
            if not os.path.exists(illustration_path):
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (800, 800), color='#f0f0f0')
                draw = ImageDraw.Draw(img)
                draw.text((400, 400), "Illustration Placeholder", fill='#333333', anchor='mm')
                os.makedirs(os.path.dirname(illustration_path), exist_ok=True)
                img.save(illustration_path)
        
        # Generate output path
        output_filename = f"result_{request_id}.jpg"
        output_path = os.path.join(settings.MEDIA_ROOT, 'results', output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Process personalization
        result = ai_service.process_personalization(
            photo_path=photo_path,
            illustration_path=illustration_path,
            output_path=output_path,
            position='center',
            scale=0.3
        )
        
        if result['success']:
            # Save result
            personalization_request.result_image = f'results/{output_filename}'
            personalization_request.face_confidence = result.get('face_confidence')
            personalization_request.status = 'completed'
            personalization_request.error_message = None
        else:
            personalization_request.status = 'failed'
            personalization_request.error_message = result.get('error', 'Unknown error')
        
        personalization_request.save()
        
    except Exception as e:
        # Handle any unexpected errors
        try:
            personalization_request = PersonalizationRequest.objects.get(id=request_id)
            personalization_request.status = 'failed'
            personalization_request.error_message = str(e)
            personalization_request.save()
        except:
            pass


@api_view(['POST'])
def process_personalization(request, request_id):
    """
    Trigger AI processing for a personalization request
    
    POST /api/process/<request_id>/
    
    Returns:
        - 200: Processing started
        - 404: Request not found
        - 400: Invalid state
    """
    try:
        personalization_request = PersonalizationRequest.objects.get(id=request_id)
    except PersonalizationRequest.DoesNotExist:
        return Response(
            {'error': 'Request not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if already processing or completed
    if personalization_request.status in ['processing', 'completed']:
        return Response(
            {'error': f'Request is already {personalization_request.status}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Start processing in background thread
    thread = threading.Thread(target=process_in_background, args=(request_id,))
    thread.daemon = True
    thread.start()
    
    return Response(
        {
            'message': 'Processing started',
            'request_id': request_id,
            'status': 'processing'
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_result(request, request_id):
    """
    Get the result of a personalization request
    
    GET /api/result/<request_id>/
    
    Returns:
        - 200: Request details with result if completed
        - 404: Request not found
    """
    try:
        personalization_request = PersonalizationRequest.objects.get(id=request_id)
    except PersonalizationRequest.DoesNotExist:
        return Response(
            {'error': 'Request not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PersonalizationRequestSerializer(personalization_request)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_requests(request):
    """
    List all personalization requests
    
    GET /api/requests/
    
    Returns:
        - 200: List of all requests
    """
    requests = PersonalizationRequest.objects.all()
    serializer = PersonalizationRequestSerializer(requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
