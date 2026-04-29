import cv2
import torch
from pathlib import Path
from ultralytics import YOLO

def detect_helmet(image_path):
    """
    输入图片路径，使用runs中最好的模型检测头盔，
    返回是否戴头盔以及标注后的图片（BGR格式）。
    """
    # 自动找到runs/train目录下最佳模型
    
    best_model_path = list(Path('runs/detect/helmet_detection/helmet_yolo11n').rglob('weights/best.pt'))
    if not best_model_path:
        raise FileNotFoundError("未在 runs/train 下找到 best.pt 模型文件")
    model_path = str(best_model_path[0])

    # 加载模型
    model = YOLO(model_path)

    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"无法读取图片: {image_path}")

    # 推理
    results = model(img)[0]

    has_helmet = False
    max_conf = 0.0
    # 绘制检测框
    if results.boxes is not None:
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            # 假设头盔类别id为0（通常头盔类别为0，可根据实际调整）
            if cls_id == 0 and conf > 0.5:
                has_helmet = True
                max_conf = max(max_conf, conf)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, f'Helmet {conf:.2f}', (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    print('识别成功')
    return has_helmet, max_conf, img
