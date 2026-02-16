import sys
import os
import cv2
import numpy as np
from hivision.creator.face_detector import FaceDetector
from hivision.creator.human_matting import HumanMatting
from hivision.creator.photo_adjuster import PhotoAdjuster

# 初始化模型 (单例模式，避免重复加载)
class AIProcessor:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.face_detector = FaceDetector(os.path.join(base_path, "hivision/creator/weights/face_detector"))
        self.human_matting = HumanMatting(os.path.join(base_path, "hivision/creator/weights/human_matting"))
        self.adjuster = PhotoAdjuster()

    def process_image(self, image_bytes, size=(413, 295), bg_color=(255, 255, 255)):
        # 1. 转换图片格式
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 2. 人脸检测
        faces, _ = self.face_detector.detect(img)
        if not faces:
            return None, "No face detected"
            
        # 3. 抠图 & 换底 & 裁剪 (这里简化调用流程，实际需要对接 Hivision 的完整 pipeline)
        # 注意：这里为了演示，暂时只做简单抠图，完整逻辑需迁移 app.py 中的 IDPhotoProcessor
        
        mask = self.human_matting.get_mask(img)
        # TODO: 完整证件照生成逻辑
        
        return img, "Success"

processor = AIProcessor()
