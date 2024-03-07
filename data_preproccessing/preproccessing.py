import os
import pandas as pd
import jieba
from multiprocessing import Pool
import itertools

def output_filename(file_name):
    basename, ext = os.path.splitext(file_name)
    return basename + '_cutted' + ext

def segment(text, column_name):
    return ' '.join(jieba.cut(text))

def process_row(args):
    row_tuple, column_name = args
    index, row = row_tuple
    row['分词结果'] = segment(row[column_name], column_name)
    return row[['分词结果']]

def main():
    # 从 file_name.txt 中读取多个 CSV 文件名
    try:
        with open('../Crawlers/Data/file_name.txt', 'r') as file:
            file_names = file.read().splitlines()  # 按行分割
    except FileNotFoundError:
        # 如果文件不存在，创建 file_name.txt 并退出程序
        with open('../Crawlers/Data/file_name.txt', 'w') as file:
            print("请在 file_name.txt 中提供 CSV 文件名。")
            exit()

    for file_name in file_names:
        original_csv_path = '../Crawlers/Data/csv/' + file_name
        df = pd.read_csv(original_csv_path, encoding='utf-8')
        column_name = df.columns[0]
        df[df.columns] = df[df.columns].replace(r'.*:', '', regex=True)
        df = df[df[df.columns[0]] != '评论: 3']
        with Pool(processes=4) as pool:
            result = pool.imap(process_row, itertools.product(df.iterrows(), [column_name]))
            df = pd.DataFrame(list(result))

        output_path = output_filename(file_name)
        df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()