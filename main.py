from ultralytics import YOLO

# 加载预训练模型
model = YOLO("yolo11n.pt")

# 头盔检测训练
model.train(
    data="./dataset.yaml",    # 就是刚才建的文件
    epochs=50,
    imgsz=640,
    batch=8,
    device="cpu",
    lr0=0.001,
    optimizer="Adam",
    patience=20,
    save_period=10,
    project="helmet_detection",
    name="helmet_yolo11n",
    exist_ok=True,
    pretrained=True,
)





# 加载训练好的模型
model = YOLO('runs/train/exp/weights/best.pt')

# 查看训练结果
results = model.val()  # 在验证集上评估






