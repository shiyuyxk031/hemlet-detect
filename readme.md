# 头盔检测系统 (Helmet Detection System)

基于 YOLOv11 的头盔检测系统，支持图片上传和摄像头实时检测。

## 项目结构

```
hamlet/
├── dataset.yaml                 # 数据集配置文件
├── downloaddataset.py           # 数据集下载脚本
├── filter.py                    # 数据过滤脚本
├── main.py                      # 模型训练脚本
├── testModel.py                 # 模型测试脚本
├── yolo11n.pt                   # YOLOv11 预训练权重
│
├── server/                      # 后端服务
│   ├── main.py                  # Flask API 服务入口
│   ├── imageORC.py              # 头盔检测推理逻辑
│   └── __pycache__/
│
├── helmet_detection_app/        # 前端应用
│   ├── index.html               # 主页面 (Vue3)
│   ├── test.html                # 测试页面
│   ├── vue.global.js            # Vue3 运行时
│   └── axios.min.js             # HTTP 客户端
│
├── YOLODataset/                 # 数据集
│   ├── train/
│   │   ├── images/              # 训练集图片
│   │   └── labels/              # 训练集标注
│   ├── val/
│   │   ├── images/              # 验证集图片
│   │   └── labels/              # 验证集标注
│   └── test/
│
├── runs/                        # 训练输出
│   └── detect/
│       └── helmet_detection/
│           └── helmet_yolo11n/
│               └── weights/
│                   ├── best.pt  # 最佳模型权重
│                   ├── last.pt  # 最新模型权重
│                   └── epoch*.pt
│
├── uploads/                     # 上传图片临时目录
├── output/                      # 输出目录
├── models/                      # 模型目录
│
└── readme.md                    # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors ultralytics opencv-python torch
```

### 2. 训练模型

```bash
python main.py
```

### 3. 启动后端服务

```bash
python server/main.py
```

后端运行在 `http://127.0.0.1:5000`

### 4. 启动前端

```bash
# 在 helmet_detection_app 目录下启动一个简单的 HTTP 服务器
cd helmet_detection_app
python -m http.server 8080
```

然后浏览器访问 `http://127.0.0.1:8080`

## API 接口

### POST /predict
上传图片进行头盔检测

- 请求: `multipart/form-data`，字段 `file`
- 响应:
  ```json
  {
    "success": true,
    "has_helmet": true,
    "confidence": 0.95,
    "image_base64": "...",
    "message": "检测到安全帽"
  }
  ```

### GET /health
健康检查
