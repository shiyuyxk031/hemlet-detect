from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from werkzeug.utils import secure_filename
import cv2
from imageORC import detect_helmet

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 允许跨域请求
# 配置
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400

        file = request.files['file']

        # 2. 检查文件名是否为空
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        # 3. 检查文件格式
        if not allowed_file(file.filename):
            return jsonify({'error': '文件格式不支持，请上传PNG、JPG、JPEG或GIF格式的图片'}), 400

        # 4. 保存文件
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 5. 执行头盔检测
        has_helmet, confidence, annotated_image = detect_helmet(file_path)

                        # 6. 将标注图片转为base64
        _, buffer = cv2.imencode('.jpg', annotated_image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # 7. 删除上传的临时文件
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            'success': True,
            'has_helmet': has_helmet,
            'confidence': confidence,
            'image_base64': img_base64,
            'message': '检测到安全帽' if has_helmet else '未检测到安全帽'
        })

    except FileNotFoundError as e:
        print(f"模型文件未找到: {e}")
        return jsonify({'error': '模型文件未找到，请检查模型路径'}), 500
    except Exception as e:
        print(f"预测错误: {e}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

