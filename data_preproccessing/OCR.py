import os
import paddleocr as ocr

def ocr_paddle(img_path):
     ocr_instance = ocr.PaddleOCR(use_angle_cls=True, lang='ch')  # 根据参数设置初始化 OCR 实例
     result = ocr_instance.ocr(img_path, cls=True)  # 使用 OCR 实例识别图片中的文字
     return result  # 返回识别结果

# 获取同一目录下的所有png文件
img_dir = './png'
img_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith('.png')]

with open('output.txt', 'w') as f:  # 以写入模式打开一个名为output.txt的文件
    for img_file in img_files:
        result = ocr_paddle(img_file)  # 获取OCR识别的结果
        for line in result:
            f.write('\n'.join([str(word_info[-1][0]) for word_info in line]) + '\n')  # 将识别的结果写入到文件中