"""
AI Processing Service for Photo Personalization

This module handles:
1. Face detection using OpenCV Haar Cascade
2. Face stylization using LOCAL OpenCV cartoon filter (NO API required)
3. Face insertion into illustrations using Pillow/OpenCV

100% FREE - No external API dependencies!
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


class AIPersonalizationService:
    """Service for LOCAL photo personalization (no API required)"""
    
    def __init__(self):
        """Initialize OpenCV face detection"""
        # Load OpenCV's pre-trained Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
    
    def detect_face(self, image_path):
        """
        Detect face in the uploaded photo using OpenCV
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Face bounding box coordinates and confidence
                  {x, y, width, height, confidence}
            None: If no face detected
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # Get the largest face (most prominent)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        return {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h),
            'confidence': 0.95  # OpenCV doesn't provide confidence, use default
        }
    
    def crop_face_with_padding(self, image_path, face_bbox, padding=0.3):
        """
        Crop face from image with padding
        
        Args:
            image_path: Path to the image
            face_bbox: Face bounding box dict
            padding: Padding ratio (0.3 = 30% padding)
            
        Returns:
            PIL.Image: Cropped face image
        """
        image = Image.open(image_path)
        
        # Calculate padding
        pad_w = int(face_bbox['width'] * padding)
        pad_h = int(face_bbox['height'] * padding)
        
        # Calculate crop box with padding
        left = max(0, face_bbox['x'] - pad_w)
        top = max(0, face_bbox['y'] - pad_h)
        right = min(image.width, face_bbox['x'] + face_bbox['width'] + pad_w)
        bottom = min(image.height, face_bbox['y'] + face_bbox['height'] + pad_h)
        
        # Crop and return
        return image.crop((left, top, right, bottom))
    
    def cartoonify_face(self, face_image):
        """
        Apply cartoon effect using LOCAL OpenCV processing (NO API required)
        
        This creates a cartoon/illustration style using:
        1. Bilateral filtering for edge-preserving smoothing
        2. Edge detection using adaptive thresholding
        3. Color quantization to reduce colors
        4. Combining edges with quantized colors
        
        Args:
            face_image: PIL Image of the cropped face
            
        Returns:
            PIL.Image: Cartoonified face image
        """
        # Convert PIL image to OpenCV format
        img_array = np.array(face_image)
        img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Step 1: Apply bilateral filter for edge-preserving smoothing
        # This smooths flat regions while keeping edges sharp
        num_bilateral = 7
        for _ in range(num_bilateral):
            img = cv2.bilateralFilter(img, d=9, sigmaColor=9, sigmaSpace=7)
        
        # Step 2: Detect edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2
        )
        
        # Step 3: Color quantization (reduce number of colors)
        # Convert to float
        data = np.float32(img).reshape((-1, 3))
        
        # Define criteria and apply kmeans
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        k = 9  # Number of colors
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert back to 8 bit values
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()]
        quantized = quantized.reshape(img.shape)
        
        # Step 4: Combine edges with quantized image
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(quantized, edges_colored)
        
        # Enhance the result
        cartoon = cv2.detailEnhance(cartoon, sigma_s=10, sigma_r=0.15)
        
        # Convert back to PIL Image
        cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        cartoon_pil = Image.fromarray(cartoon_rgb)
        
        return cartoon_pil
    
    def insert_face_into_illustration(self, stylized_face, illustration_path, 
                                     position='center', scale=1.0):
        """
        Insert stylized face into illustration
        
        Args:
            stylized_face: PIL Image of stylized face
            illustration_path: Path to the illustration
            position: Where to place face ('center', 'top', 'bottom', or tuple (x, y))
            scale: Scale factor for the face (1.0 = original size)
            
        Returns:
            PIL.Image: Final personalized illustration
        """
        # Open illustration
        illustration = Image.open(illustration_path).convert('RGBA')
        
        # Resize stylized face
        face_width = int(stylized_face.width * scale)
        face_height = int(stylized_face.height * scale)
        stylized_face = stylized_face.resize((face_width, face_height), Image.LANCZOS)
        
        # Ensure stylized face has alpha channel
        if stylized_face.mode != 'RGBA':
            stylized_face = stylized_face.convert('RGBA')
        
        # Calculate position
        if position == 'center':
            x = (illustration.width - face_width) // 2
            y = (illustration.height - face_height) // 2
        elif position == 'top':
            x = (illustration.width - face_width) // 2
            y = illustration.height // 4
        elif position == 'bottom':
            x = (illustration.width - face_width) // 2
            y = (illustration.height * 3) // 4 - face_height
        elif isinstance(position, tuple):
            x, y = position
        else:
            x = (illustration.width - face_width) // 2
            y = (illustration.height - face_height) // 2
        
        # Create a copy of illustration
        result = illustration.copy()
        
        # Paste stylized face onto illustration
        result.paste(stylized_face, (x, y), stylized_face)
        
        return result.convert('RGB')
    
    def process_personalization(self, photo_path, illustration_path, 
                               output_path, position='center', scale=0.3):
        """
        Complete personalization pipeline
        
        Args:
            photo_path: Path to child's photo
            illustration_path: Path to illustration template (not used in current implementation)
            output_path: Where to save the result
            position: Where to place the face (not used - kept for compatibility)
            scale: Scale factor for the face (not used - kept for compatibility)
            
        Returns:
            dict: Processing result with status and details
        """
        try:
            # Step 1: Detect face (for confidence reporting)
            face_bbox = self.detect_face(photo_path)
            if not face_bbox:
                return {
                    'success': False,
                    'error': 'No face detected in the photo. Please upload a clear photo with a visible face.'
                }
            
            # Step 2: Load the entire original photo
            original_photo = Image.open(photo_path)
            
            # Step 3: Apply cartoon filter to the ENTIRE photo (not just face)
            # This preserves the original photo dimensions
            cartoonified_photo = self.cartoonify_face(original_photo)
            
            # Step 4: Save result (same size as original photo)
            cartoonified_photo.save(output_path, 'JPEG', quality=95)
            
            return {
                'success': True,
                'output_path': output_path,
                'face_confidence': face_bbox['confidence']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
