# 使用kagglehub库（推荐）
import kagglehub

# 下载头盔数据集
path = kagglehub.dataset_download("andrewmvd/helmet-detection")
print("下载路径:", path)

# 复制到helmetDataset
import shutil
import os

dataset_name = "helmetDataset"
os.makedirs(dataset_name, exist_ok=True)

for item in os.listdir(path):
    src = os.path.join(path, item)
    dst = os.path.join(dataset_name, item)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)

print(f"数据集已保存到 {dataset_name} 文件夹")