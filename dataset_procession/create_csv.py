import pandas as pd
import os

#创建csv文件
def create_csv():
    #创建文件夹
    if not os.path.exists('../dataset_procession/Data/csv'):
        os.makedirs('../dataset_procession/Data/csv')
    #创建csv文件,gbk编码
    df = pd.DataFrame(columns=['content','summary'])
    df.to_csv('../dataset_procession/Data/csv/data.csv',index=False,encoding='gbk')

create_csv()