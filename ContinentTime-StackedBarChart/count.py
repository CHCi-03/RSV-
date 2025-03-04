#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import re
import pandas as pd
from openpyxl import load_workbook

def extract_year(s):
    """从字符串中提取末尾4位年份"""
    match = re.search(r'(\d{4})$', str(s))
    return match.group(1) if match else None

def process_files(folder_path, output_file):
    # 获取所有Excel文件
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    
    # 存储所有年份和文件统计
    all_years = set()
    stats = {}
    
    # 处理每个文件
    for file in files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path, header=None)  # 无表头读取
        
        # 提取年份并统计
        years = df[0].apply(extract_year).dropna()
        year_counts = years.value_counts().to_dict()
        
        # 更新全局数据
        all_years.update(year_counts.keys())
        stats[file.replace('.xlsx', '')] = year_counts
    
    # 创建结果DataFrame
    result_df = pd.DataFrame(
        index=sorted(all_years, key=lambda x: int(x)),
        columns=sorted(stats.keys())
    ).fillna(0)
    
    # 填充数据
    for file, counts in stats.items():
        for year, count in counts.items():
            result_df.loc[year, file] = count
    
    # 保存结果
    result_df.to_excel(output_file, sheet_name='Yearly Statistics')
    print(f'结果已保存至：{output_file}')

# 使用示例
folder_path = r'F:\Desktop\respiratory syncytial virus\AB时间大洲细分Excel表\Figure1\B'
output_path = r'F:\Desktop\respiratory syncytial virus\AB时间大洲细分Excel表\Figure1\B-Yearly_Statistics.xlsx'
process_files(folder_path, output_path)


# In[ ]:




