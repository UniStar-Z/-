import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np

# 加载预训练的深度学习模型
model_path = 'models/defect_detection_model.pth'  # 模型路径，可能需要修改此路径
model = torch.load(model_path, map_location=torch.device('cpu'))
model.eval()

def preprocess_image(image_path):
    """预处理图像，使其适合模型输入"""
    image = Image.open(image_path).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),  # 调整为模型输入尺寸，可能需要修改此尺寸
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = preprocess(image)
    image = image.unsqueeze(0)  # 增加批次维度
    return image

def detect_defects(image_path):
    """使用深度学习模型检测图像中的缺陷"""
    image = preprocess_image(image_path)
    with torch.no_grad():
        predictions = model(image)
    predictions = torch.sigmoid(predictions).numpy()
    defects = []

    # 假设模型输出为多个类别的概率
    defect_types = ['scratch', 'inclusion', 'crack', 'dent']  # 缺陷类型，可能需要修改此列表
    for i, defect_type in enumerate(defect_types):
        if predictions[0][i] > 0.5:
            defects.append({'type': defect_type, 'confidence': float(predictions[0][i])})

    return defects