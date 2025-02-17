from typing import List, Tuple
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
from transformers import pipeline

class ImageFilter:
    def __init__(self):
        """
        Initialize the image filter with required models.
        """
        # Load NSFW detection model from transformers
        self.nsfw_classifier = pipeline(
            "image-classification",
            model="Falconsai/nsfw_image_detection",
            top_k=5
        )
        
        # Load violence detection model
        self.violence_classifier = pipeline(
            "image-classification",
            model="microsoft/resnet-50",
            top_k=5
        )
        
        # Initialize detection thresholds
        self.nsfw_threshold = 0.7
        self.violence_threshold = 0.7
        
        # Define inappropriate content categories
        self.inappropriate_categories = {
            'NSFW': ['porn', 'hentai', 'sexy', 'drawings', 'neutral'],
            'Violence': ['blood', 'weapon', 'injury', 'fighting'],
            'Offensive': ['hate_symbol', 'offensive_gesture']
        }
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for model input.
        """
        # Convert to RGB if needed
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        
        # Resize image while maintaining aspect ratio
        max_size = 800
        ratio = min(max_size/image.size[0], max_size/image.size[1])
        new_size = tuple([int(dim * ratio) for dim in image.size])
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def _check_nsfw_content(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Check if image contains NSFW content.
        Returns (is_inappropriate, category).
        """
        try:
            # Get predictions
            predictions = self.nsfw_classifier(image)
            
            # Check predictions
            for pred in predictions:
                label = pred['label'].lower()
                score = pred['score']
                
                # If it's porn or hentai with high confidence, definitely inappropriate
                if label in ['porn', 'hentai'] and score > self.nsfw_threshold:
                    return True, f"NSFW: {label}"
                
                # If it's sexy content with high confidence, also inappropriate
                if label == 'sexy' and score > self.nsfw_threshold:
                    return True, f"NSFW: {label}"
            
            return False, ""
            
        except Exception as e:
            print(f"Warning: Error in NSFW detection: {str(e)}")
            return True, "Error in processing"  # Err on the side of caution
    
    def _check_violence_content(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Check if image contains violent content.
        Returns (is_inappropriate, category).
        """
        try:
            # Convert image to numpy array for OpenCV processing
            img_np = np.array(image)
            
            # Check for blood (red color detection)
            hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
            lower_red = np.array([0, 120, 70])
            upper_red = np.array([10, 255, 255])
            red_mask = cv2.inRange(hsv, lower_red, upper_red)
            
            # If significant red areas detected, might be blood
            red_ratio = np.sum(red_mask > 0) / (image.size[0] * image.size[1])
            if red_ratio > 0.2:  # If more than 20% is red
                return True, "Violence: Blood detected"
            
            # Use violence classifier
            predictions = self.violence_classifier(image)
            for pred in predictions:
                label = pred['label'].lower()
                score = pred['score']
                
                if any(category in label for category in ['weapon', 'knife', 'gun', 'blood', 'injury']) and score > self.violence_threshold:
                    return True, f"Violence: {label}"
            
            return False, ""
            
        except Exception as e:
            print(f"Warning: Error in violence detection: {str(e)}")
            return False, ""  # Don't flag if violence check fails
    
    def _is_inappropriate(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Check if image contains inappropriate content.
        Returns (is_inappropriate, category).
        """
        try:
            # Preprocess image
            processed_image = self._preprocess_image(image)
            
            # Check for NSFW content
            is_nsfw, nsfw_category = self._check_nsfw_content(processed_image)
            if is_nsfw:
                return True, nsfw_category
            
            # Check for violent content
            is_violent, violence_category = self._check_violence_content(processed_image)
            if is_violent:
                return True, violence_category
            
            return False, ""
            
        except Exception as e:
            print(f"Warning: Error processing image: {str(e)}")
            return True, "Error in processing"  # Err on the side of caution
    
    def filter_image(self, image: Image.Image) -> Tuple[Image.Image, bool, str]:
        """
        Filter an image by checking for inappropriate content.
        Returns (filtered_image, was_inappropriate, category).
        """
        try:
            was_inappropriate, category = self._is_inappropriate(image)
            
            if was_inappropriate:
                print(f"Removed inappropriate image: {category}")
                return None, True, category
            
            return image, False, ""
            
        except Exception as e:
            print(f"Warning: Error filtering image: {str(e)}")
            return None, True, "Error in processing"
    
    def filter_images(self, images: List[Image.Image]) -> Tuple[List[Image.Image], List[bool], List[str]]:
        """
        Filter a list of images by removing inappropriate ones.
        Returns (filtered_images, flags, categories).
        """
        filtered_images = []
        flags = []
        categories = []
        
        for image in images:
            filtered_image, was_flagged, category = self.filter_image(image)
            if filtered_image is not None:
                filtered_images.append(filtered_image)
            flags.append(was_flagged)
            categories.append(category)
        
        return filtered_images, flags, categories
    
    def get_image_stats(self, flags: List[bool], categories: List[str]) -> dict:
        """
        Get detailed statistics about filtered images.
        """
        total_images = len(flags)
        flagged_images = sum(flags)
        
        # Count by category
        category_counts = {}
        for category in categories:
            if category:  # Only count non-empty categories
                main_category = category.split(':')[0].strip()
                category_counts[main_category] = category_counts.get(main_category, 0) + 1
        
        return {
            "total_images": total_images,
            "flagged_images": flagged_images,
            "clean_ratio": (total_images - flagged_images) / total_images if total_images > 0 else 1.0,
            "categories": category_counts
        } 