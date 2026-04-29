import os
import shutil

# ===================== 你只需要改这里 =====================
FOLDER_A = "a"  # 来源文件夹（取前缀）
FOLDER_B = "b"  # 目标文件夹（匹配文件）
OUTPUT_FOLDER = "matched_result"  # 输出文件夹（自动创建）
# ==========================================================

# 创建输出文件夹
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# 1. 获取 a 文件夹里所有文件的前缀（去掉后缀）
prefix_set = set()
for filename in os.listdir(FOLDER_A):
    # 跳过文件夹，只处理文件
    file_path = os.path.join(FOLDER_A, filename)
    if not os.path.isfile(file_path):
        continue

    # 提取前缀（如 123.jpg → 123）
    prefix = os.path.splitext(filename)[0]
    prefix_set.add(prefix)

print(f"✅ 从 a 文件夹提取到 {len(prefix_set)} 个前缀")

# 2. 遍历 b 文件夹，匹配前缀并复制
count = 0
for filename in os.listdir(FOLDER_B):
    file_path = os.path.join(FOLDER_B, filename)
    if not os.path.isfile(file_path):
        continue

    # 提取当前文件前缀
    b_prefix = os.path.splitext(filename)[0]

    # 如果前缀在 a 的前缀集合里 → 复制
    if b_prefix in prefix_set:
        src = file_path
        dst = os.path.join(OUTPUT_FOLDER, filename)
        shutil.copy2(src, dst)  # 复制文件（不删除原文件）
        count += 1
        print(f"📌 已匹配：{filename}")

print("\n" + "=" * 50)
