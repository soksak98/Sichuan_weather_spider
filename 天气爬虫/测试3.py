import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'Host': 'lishi.tianqi.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
}

# 定义要爬取的城市列表和对应的拼音
cities = {
    'leshan': '乐山',
    'chongqing': '重庆',
    'kangding': '康定',
    'yaan': '雅安',
    'langzhong': '阆中',
    'chengdu': '成都',
    'hechuan': '合川'  # 新增的城市
}

# 定义要爬取的年份范围和每个月份的天数
year_range = [2019, 2020, 2021, 2022, 2023]
month_days = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}

# 创建存储数据的文件夹
output_folder = '城市天气数据'
os.makedirs(output_folder, exist_ok=True)

# 循环爬取每个城市在五年间每个月的天气数据
for city_key, city_name in cities.items():
    city_folder = os.path.join(output_folder, city_name)
    os.makedirs(city_folder, exist_ok=True)

    for year in year_range:
        for month in range(1, 13):  # 从1月到12月
            if month <= month_days.get(2, 28 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 29):
                url = f'https://lishi.tianqi.com/{city_key}/{year}{month:02d}.html'
            else:
                url = f'https://lishi.tianqi.com/{city_key}/{year}{month:02d}.html'

            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            html = BeautifulSoup(res.text, 'html.parser')

            data_all = []
            tian_three = html.find("div", {"class": "tian_three"})
            if tian_three:
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

                # 保存到 CSV 文件，文件名包含对应的城市、年份和月份信息
                file_name = f"{city_name}_{year}年{month}月天气.csv"
                file_path = os.path.join(city_folder, file_name)
                weather_df.to_csv(file_path, encoding="utf-8-sig", index=False)

                print(f"已保存 {file_path}")

print("所有数据已保存完成。")
