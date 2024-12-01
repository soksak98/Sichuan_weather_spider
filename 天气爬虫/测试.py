import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'Host': 'lishi.tianqi.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
}

# 定义要爬取的年份列表
years = ['2020', '2021', '2022', '2023', '2024']

# 循环爬取每个年份的1月份天气数据
for year in years:
    url = f'https://lishi.tianqi.com/huhehaote/{year}01.html'  # 构造每年1月份的天气数据链接
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    html = BeautifulSoup(res.text, 'html.parser')

    data_all = []
    tian_three = html.find("div", {"class": "tian_three"})
    lishi = tian_three.find_all("li")

    for item in lishi:
        data = []
        for j in item.find_all("div"):
            data.append(j.text.strip())
        data_all.append(data)

    # 创建 DataFrame
    weather_df = pd.DataFrame(data_all, columns=["当日信息", "最高气温", "最低气温", "天气", "风向信息"])

    # 提取日期和星期信息
    result = pd.DataFrame(weather_df['当日信息'].apply(lambda x: pd.Series(str(x).split(' '))))
    result.columns = ['日期', '星期']
    result1 = pd.DataFrame(weather_df['风向信息'].apply(lambda x: pd.Series(str(x).split(' '))))
    result1.columns = ['风向', '级数']

    # 整合数据
    weather_df = weather_df.drop(columns=['当日信息', '风向信息'])
    weather_df.insert(loc=0, column='日期', value=result['日期'])
    weather_df.insert(loc=1, column='星期', value=result['星期'])
    weather_df.insert(loc=5, column='风向', value=result1['风向'])
    weather_df.insert(loc=6, column='级数', value=result1['级数'])

    # 保存到 CSV 文件，文件名包含对应的年份
    file_name = f"呼和浩特{year}年1月天气.csv"
    weather_df.to_csv(file_name, encoding="utf-8-sig", index=False)

    print(f"已保存 {file_name}")

print("所有数据已保存完成。")
