import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体，以便在图表中显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取CSV文件
df = pd.read_csv('雅安')

# 将日期和年份合并为一个列，并转换为pandas的日期类型
df['日期'] = pd.to_datetime(df['日期'] + '-' + df['年份'].astype(str))

# 删除原来的年份列
df = df.drop(columns=['年份'])

# 确保日期列是按顺序的
df = df.sort_values(by='日期')

# 设置日期为索引
df.set_index('日期', inplace=True)

# 创建一个图形和一组子图
fig, axs = plt.subplots(3, 2, figsize=(15, 15))

# 绘制最高气温和最低气温的折线图
axs[0, 0].plot(df['最高气温'], label='最高气温')
axs[0, 0].plot(df['最低气温'], label='最低气温')
axs[0, 0].set_title('最高气温和最低气温变化')
axs[0, 0].legend()

# 绘制天气分类的扇形图
weather_counts = df['天气分类'].value_counts()
axs[0, 1].pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%')
axs[0, 1].set_title('天气分类分布')

# 绘制风向的柱状图
wind_direction_counts = df['风向'].value_counts()
axs[1, 0].bar(wind_direction_counts.index, wind_direction_counts.values)
axs[1, 0].set_title('风向分布')

# 绘制风级数的柱状图
wind_speed_counts = df['级数'].value_counts()
axs[1, 1].bar(wind_speed_counts.index, wind_speed_counts.values)
axs[1, 1].set_title('风级数分布')

# 绘制是否特殊的扇形图
special_counts = df['是否特殊'].value_counts()
axs[2, 0].pie(special_counts, labels=special_counts.index, autopct='%1.1f%%')
axs[2, 0].set_title('是否特殊天气分布')

# 调整子图间距
plt.tight_layout()

# 显示图表
plt.show()