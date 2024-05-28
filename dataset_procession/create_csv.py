"""
CSVCreator - 用于创建CSV文件的类

这个类封装了创建CSV文件的功能，提供了一个简单的接口来生成一个空的CSV文件。

类方法说明：
__init__(self):
- 初始化CSVCreator实例。

create_csv(self):
- 创建一个空的CSV文件，如果指定的文件夹不存在，则创建文件夹。
- 默认创建一个包含'content'和'summary'列的DataFrame，并保存到'../dataset_procession/Data/csv/data.csv'。

使用方法：
1. 创建CSVCreator实例。
2. 调用create_csv方法来生成CSV文件。

注意：
- 该类依赖于pandas库来创建DataFrame。
- 默认情况下，CSV文件将使用GBK编码。
- CSV文件将被保存在'../dataset_procession/Data/csv/data.csv'。
"""

import pandas as pd
import os
import sys

class CSVCreator:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def create_csv(self):
        """创建一个空的CSV文件"""
        # 创建文件夹
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # 创建csv文件, gbk编码
        df = pd.DataFrame(columns=['content', 'summary'])
        csv_path = os.path.join(self.output_dir, 'data.csv')
        df.to_csv(csv_path, index=False, encoding='gbk')
        print(f"CSV file created at: {csv_path}")

# 使用示例
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_csv.py <output_directory>")
        sys.exit(1)

    output_directory = sys.argv[1]
    creator = CSVCreator(output_directory)
    creator.create_csv()
