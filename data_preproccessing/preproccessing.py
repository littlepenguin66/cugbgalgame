import os
import pandas as pd
import jieba
from multiprocessing import Pool

# 填写data路径下原始csv名称
file_name = 'tieba.csv'
original_csv_path = '../Crawlers/Data/' + file_name
df = pd.read_csv(original_csv_path, encoding='utf-8')
column_name = df.columns[0]

def output_filename(file_name):
    basename, ext = os.path.splitext(file_name)
    return basename + '_cutted' + ext

def segment(text, column_name):
    return ' '.join(jieba.cut(text))

def process_row(row_tuple):
    index, row = row_tuple
    row['分词结果'] = segment(row[column_name], column_name)
    return row[['分词结果']]  # Only return the '分词结果' column

def main():
    original_csv_path = '../Crawlers/Data/' + file_name
    df = pd.read_csv(original_csv_path, encoding='utf-8')
    df[df.columns] = df[df.columns].replace(r'回复.*?:', '', regex=True)

    with Pool(processes=4) as pool:
        result = pool.imap(process_row, df.iterrows())
        df = pd.DataFrame(list(result))

    output_path = output_filename(file_name)
    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()