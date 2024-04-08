import pandas as pd
import json

def read_csv():
    df = pd.read_csv('../dataset_procession/Data/csv/data.csv',encoding='gbk')
    print(df)
    to_json(df)

def to_json(df):
    # 将df转为字典列表
    new_rows = []
    for _, row in df.iterrows():
        content = row['content']
        summary = row['summary']
        content1 = f'什么是{content}'
        content2 = f'{content}是什么'
        content3 = f'{content}是什么意思'
        content4 = f'{content}的意思'
        content5 = f'介绍一下{content}'
        content6 = f'啥是{content}'
        content7 = f'{content}是啥'
        content8 = f'{content}是啥意思'
        content9 = f'{content}的意思是什么'
        for i in range (1,10):
            new_content = locals()[f'content{i}']
            new_rows.append({'content': new_content, 'summary': summary})
    new_df = pd.DataFrame(new_rows)
    data_dict = new_df.to_dict('records')
    # 保存为json文件，每个对象换行
    with open('../dataset_procession/Data/json/data.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

read_csv()
