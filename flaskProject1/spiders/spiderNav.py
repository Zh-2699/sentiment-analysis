import requests
import csv
import numpy as np
import os
import re

def init():
    # 初始化 CSV 文件，如果文件不存在则创建
    if not os.path.exists("./navData.csv"):
        with open('./navData.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'TypeName',
                'gid',
                'containerid',
            ])

def clean_data(text):
    # 去除不可见字符
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

def load_existing_data():
    # 读取 CSV 文件中已有的数据，并返回一个集合
    existing_data = set()
    if os.path.exists("./navData.csv"):
        with open('./navData.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳过标题行
            for row in reader:
                # 将每行数据转换为元组并添加到集合中
                existing_data.add((row[0], row[1], row[2]))
    return existing_data

def writerRow(row, existing_data):
    # 检查数据是否已经存在，如果不存在则写入
    row_tuple = (row[0], row[1], row[2])
    if row_tuple not in existing_data:
        with open('./navData.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

def getNavData(url):
    headers = {
        'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWm2Y1HFfkWlN0PLpZ_MOoT5JpX5KMhUgL.Fo-71heESheRS0B2dJLoI7DVwg_awg8X9g44; SINAGLOBAL=5508538758124.011.1735751090248; ULV=1736330635505:28:2:1:2123460227276.8145.1736330635489:1735751090250; XSRF-TOKEN=V1rRsKCDAsiue6YTGszwlswa; ALF=1738991594; SUB=_2A25Keyq6DeRhGeNO41ET9C3EzDiIHXVp-SJyrDV8PUJbkNANLWj7kW1NTttMbkTR86z71BMISkFIDvXLGBtpmTZr; WBPSESS=0Hgcmu6MbMQzjQhdRMoliXGk8m6TOWklOqsGzR49K-zLt54XcQhBnjh1BUEMe9ws44uSIzVp2RcAWc0HBi6Qckf0ANp9XpnoHzrWc6R8cQ-9ASXLHZT-QzXe-XEEHPGRm3jPgTKDEZi2ivBVBrl9fA==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }
    params = {
        'is_new_segment': 1,
        'fetch_hot': 1,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response, existing_data):
    # 解析 JSON 数据并写入 CSV 文件
    navList = np.append(response['groups'][3]['group'], response['groups'][4]['group'])
    for nav in navList:
        navName = clean_data(nav['title'])
        gid = str(int(float(nav['gid'])))  # 处理科学计数法
        containerid = clean_data(nav['containerid'])
        writerRow([
            navName,
            gid,
            containerid,
        ], existing_data)

if __name__ == '__main__':
    init()
    url = 'https://weibo.com/ajax/feed/allGroups'
    response = getNavData(url)
    if response:
        # 加载现有数据
        existing_data = load_existing_data()
        # 解析并写入新数据
        parse_json(response, existing_data)