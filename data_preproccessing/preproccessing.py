import pandas as pd
import jieba
from multiprocessing import Pool

def segment(text):
    return ' '.join(jieba.cut(text))

def process_row(row_tuple):
    index, row = row_tuple
    row['分词结果'] = segment(row['唯一满分 玻璃t0 易拉罐t0.5 但打开大瓶装放时间久了是粪水'])
    return row

def main():
    original_csv_path = 'tieba2024.csv'
    df = pd.read_csv(original_csv_path, encoding='utf-8')
    df[df.columns] = df[df.columns].replace(r'回复.*?:', '', regex=True)

    with Pool(processes=8) as pool:
        result = pool.imap(process_row, df.iterrows())
        df = pd.DataFrame(result)

    output_path = 'tieba_segmented_cut.csv'
    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()