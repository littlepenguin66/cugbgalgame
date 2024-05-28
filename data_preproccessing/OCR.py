"""
PaddleOCRWrapper - 用于封装PaddleOCR的类，优化代码结构

这个类封装了PaddleOCR的功能，提供了一个更简洁的接口来处理图像识别。

类方法说明：
__init__(use_angle_cls=True, lang='ch'):
- 初始化PaddleOCRWrapper实例。
- 根据提供的参数设置初始化OCR实例。

ocr_image(img_path):
- 使用OCR实例识别图片中的文字。
- 返回识别结果。

process_directory(img_dir):
- 处理指定目录下的所有PNG文件。
- 将识别的结果写入到output.txt文件中。

使用方法：
1. 创建PaddleOCRWrapper实例。
2. 调用process_directory方法，传入包含PNG文件的目录路径。
3. 输出结果将被写入到output.txt文件中。

注意：
- 该类依赖于paddleocr库来进行图像识别。
- process_directory方法会处理指定目录下的所有PNG文件。
- 识别结果以文本形式写入到output.txt文件中，每行包含一个识别的文字。
"""

import os
import sys
import paddleocr as ocr

class PaddleOCRWrapper:
    def __init__(self, use_angle_cls=True, lang='ch'):
        self.ocr_instance = ocr.PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)

    def ocr_image(self, img_path):
        result = self.ocr_instance.ocr(img_path, cls=True)
        return result

    def process_directory(self, img_dir, output_file):
        img_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith('.png')]
        with open(output_file, 'w') as f:
            for img_file in img_files:
                result = self.ocr_image(img_file)
                for line in result:
                    f.write('\n'.join([str(word_info[-1][0]) for word_info in line]) + '\n')

# 使用示例
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python OCR.py <img_directory> <output_file>")
    else:
        img_directory = sys.argv[1]
        output_file = sys.argv[2]
        ocr_wrapper = PaddleOCRWrapper()
        ocr_wrapper.process_directory(img_directory, output_file)
