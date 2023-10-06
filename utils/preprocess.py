import cv2
import numpy as np
import os
import time


def crop_image(image, crop_percent):
    # Get the original image dimensions
    height, width = image.shape[:2]

    # Calculate the crop values based on the crop_percent
    crop_height = int(height * crop_percent)
    crop_width = int(width * crop_percent)

    # Calculate the crop boundaries
    top = crop_height
    bottom = height - crop_height
    left = crop_width
    right = width - crop_width

    # Crop the image
    cropped_image = image[top:bottom, left:right]

    return cropped_image


def resize_image(image, target_size):
        # Resize the image
        resized_image = cv2.resize(image, target_size)
        return resized_image

def enhance_contrast(image):
    # Convert image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split LAB channels
    l, a, b = cv2.split(lab)

    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l)

    # Merge enhanced L channel with original A and B channels
    enhanced_lab = cv2.merge((enhanced_l, a, b))

    # Convert back to RGB color space
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    return enhanced_image


def sharpen_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (0, 0), sigmaX=1, sigmaY=1)

    # Calculate the sharpened image
    sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)

    # Convert back to color image
    sharpened_image = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)

    return sharpened_image


def apply_gaussian_blur(image, kernel_size=(3, 3), sigma=0):
    blurred_image = cv2.GaussianBlur(image, kernel_size, sigma)
    return blurred_image


def apply_median_filter(image, kernel_size=3):
    filtered_image = cv2.medianBlur(image, kernel_size)
    return filtered_image


def unsharp_masking(image, sigma=1, strength=2):
    # Apply Gaussian blur to create a blurred version of the image
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)

    # Calculate the high-pass image (original image - blurred image)
    high_pass = cv2.subtract(image, blurred)

    # Multiply the high-pass image by the strength factor
    sharpened = cv2.multiply(high_pass, strength)

    # Add the sharpened image to the original image
    sharpened_image = cv2.add(image, sharpened)

    # Make sure the pixel values are within the valid range (0-255)
    sharpened_image = np.clip(sharpened_image, 0, 255).astype(np.uint8)

    return sharpened_image


def apply_preprocess(raw_image):
    preprocessed_image = crop_image(raw_image, 0.05)
    preprocessed_image = resize_image(preprocessed_image, (1280, 720))
    preprocessed_image = enhance_contrast(preprocessed_image)
    preprocessed_image = apply_median_filter(preprocessed_image)
    preprocessed_image = unsharp_masking(preprocessed_image)

    return preprocessed_image

