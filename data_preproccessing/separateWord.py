"""
TextSegmentationProcessor - 用于对文本进行分词处理的类

这个类封装了文本分词的功能，提供了对CSV文件中指定列进行分词处理的接口。

类方法说明：
__init__(self):
- 初始化TextSegmentationProcessor实例。

segment_text(self, text, column_name):
- 对文本进行分词处理，使用空格拼接分词结果。
- 返回分词后的文本。

process_csv_file(self, file_name, column_name):
- 处理指定CSV文件中的文本，为指定列进行分词。
- 读取CSV文件，创建新列'分词结果'，并保存到新文件中。

使用方法：
1. 创建TextSegmentationProcessor实例。
2. 调用process_csv_file方法，传入CSV文件名和要分词的列名。
3. 分词后的结果将被保存到新的CSV文件中。

注意：
- 该类依赖于pandas和jieba库来进行数据处理和分词。
- process_csv_file方法会处理指定CSV文件中的文本，并保存分词结果。
- 分词结果以新的CSV文件形式保存，文件名会在原文件名后添加'_cutted'。
"""

import os
import sys
import pandas as pd
import jieba
from multiprocessing import Pool
import itertools


class TextSegmentationProcessor:
    def __init__(self):
        pass

    def segment_text(self, text):
        """对文本进行分词处理，使用空格拼接分词结果"""
        return ' '.join(jieba.cut(text))

    def process_csv_file(self, file_name, column_name):
        """处理指定CSV文件中的文本，为指定列进行分词"""
        original_csv_path = file_name
        df = pd.read_csv(original_csv_path, encoding='utf-8')
        df[df.columns] = df[df.columns].replace(r'.*:', '', regex=True)
        df = df[df[df.columns[0]] != '评论: 3']

        with Pool(processes=4) as pool:
            result = pool.imap(self.process_row, itertools.product(df.iterrows(), [column_name]))
            processed_data = list(result)

        df['分词结果'] = [item['分词结果'] for item in processed_data]
        output_path = self.output_filename(file_name)
        df.to_csv(output_path, index=False)

    def output_filename(self, file_name):
        """生成输出文件名，在原文件名后添加'_cutted'"""
        basename, ext = os.path.splitext(file_name)
        return basename + '_cutted' + ext

    def process_row(self, args):
        """处理每一行数据，为指定列进行分词，创建新列'分词结果'"""
        row_tuple, column_name = args
        index, row = row_tuple
        row['分词结果'] = self.segment_text(row[column_name])
        return row


# 使用示例
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python separateWord.py <csv_file_path> <column_name>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    column_name = sys.argv[2]

    processor = TextSegmentationProcessor()
    processor.process_csv_file(csv_file_path, column_name)
