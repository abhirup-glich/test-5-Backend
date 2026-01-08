import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np

class FaceService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceService, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.mtcnn = MTCNN(keep_all=False, device=self.device)
        self.facenet = InceptionResnetV1(pretrained="vggface2").eval().to(self.device)
    
    def get_embedding(self, image):
        # image: numpy array (opencv image)
        # returns: embedding (list) or None
        if image is None:
            return None
            
        # MTCNN expects RGB
        # If image is BGR (OpenCV default), convert to RGB? 
        # facenet_pytorch MTCNN expects PIL or numpy RGB.
        # Assuming input is numpy.
        
        # Detect face
        # mtcnn returns cropped face tensor
        img_cropped = self.mtcnn(image)
        
        if img_cropped is not None:
            # Calculate embedding
            img_embedding = self.facenet(img_cropped.unsqueeze(0))
            return img_embedding.detach().cpu().numpy()[0].tolist()
        return None

# Global instance
face_service = FaceService()
