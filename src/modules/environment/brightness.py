import cv2
import numpy as np

def get_lighting_score(image_path: str) -> float:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0.5 # Default fallback
    
    mean_brightness = np.mean(img)
    return mean_brightness / 255.0