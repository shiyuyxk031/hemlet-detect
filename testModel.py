import os
from ultralytics import YOLO
import cv2
import numpy as np

def evaluate_model(model_path, test_images_folder, ground_truth_folder=None):
    """
    评估模型性能
    """
    model = YOLO(model_path)
    
    # 1. 自动化评估
    print("=== 自动化评估 ===")
    results = model.val()
    print(f"mAP50: {results.box.map50:.4f}")
    print(f"mAP50-95: {results.box.map:.4f}")
    print(f"Precision: {float(results.box.p.mean()):.4f}")
    print(f"Recall: {float(results.box.r.mean()):.4f}")
    
    # 2. 手动检查预测结果
    print("\n=== 手动检查预测结果 ===")
    test_images = [f for f in os.listdir(test_images_folder) 
                   if f.endswith(('.jpg', '.png'))][:10]  # 检查前10张
    
    for img_name in test_images:
        img_path = os.path.join(test_images_folder, img_name)
        results = model(img_path)
        
        # 检查检测结果
        boxes = results[0].boxes
        num_detections = len(boxes)
        
        print(f"{img_name}: 检测到 {num_detections} 个目标")
        
        if num_detections > 0:
            # 获取置信度
            confidences = boxes.conf
            print(f"  置信度: {confidences}")
    
    # 3. 判断依据
import os
from ultralytics import YOLO
import cv2
import numpy as np

def evaluate_model(model_path, test_images_folder, ground_truth_folder=None):
    """
    评估模型性能
    """
    model = YOLO(model_path)

    # 1. 自动化评估
    print("=== 自动化评估 ===")
    val_results = model.val()  # val() 返回一个 list 或单个结果对象
    # 如果 val_results 是列表，取第一个元素
    if isinstance(val_results, list):
        val_result = val_results[0]
    else:
        val_result = val_results

    print(f"mAP50: {val_result.box.map50:.4f}")
    print(f"mAP50-95: {val_result.box.map:.4f}")
    print(f"Precision: {float(val_result.box.p.mean()):.4f}")
    print(f"Recall: {float(val_result.box.r.mean()):.4f}")

    # 2. 手动检查预测结果
    print("\n=== 手动检查预测结果 ===")
    test_images = [f for f in os.listdir(test_images_folder)
                   if f.endswith(('.jpg', '.png'))][:10]  # 检查前10张

    for img_name in test_images:
        img_path = os.path.join(test_images_folder, img_name)
        img_results = model(img_path)

        # 检查检测结果
        boxes = img_results[0].boxes
        num_detections = len(boxes)

        print(f"{img_name}: 检测到 {num_detections} 个目标")

        if num_detections > 0:
            # 获取置信度
            confidences = boxes.conf
            print(f"  置信度: {confidences}")

    # 3. 判断依据
    print("\n=== 评价结论 ===")
    if val_result.box.map50 > 0.85:
        print("⭐⭐⭐ 优秀！模型性能很好")
    elif val_result.box.map50 > 0.75:
        print("⭐⭐ 良好，可以部署使用")
    elif val_result.box.map50 > 0.60:
        print("⭐ 及格，需要进一步优化")
    else:
        print("❌ 需要重新训练或调整参数")

# 使用示例
evaluate_model(
    model_path='./runs/detect/helmet_detection/helmet_yolo11n/weights/best.pt',
    test_images_folder='./YOLODataset/test/images'
)
