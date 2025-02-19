"""
spiderContent.py
"""
import random
import time
import requests
import csv
import os
import re
from datetime import datetime
from random import choice

# 获取当前脚本文件所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 初始化 CSV 文件
def init():
    file_path = os.path.join(script_dir, 'articleData.csv')  # 使用绝对路径
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'likeNum', 'commentsNum', 'reportsNum', 'region', 'content',
                'contentLength', 'createdAt', 'type', 'detailUrl', 'authorAvatar',
                'authorName', 'authorDetail', 'isVip'
            ])

# 加载已存在的数据
def load_existing_data():
    file_path = os.path.join(script_dir, 'articleData.csv')  # 使用绝对路径
    existing_data = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳过标题行
            for row in reader:
                existing_data.add(row[0])  # 只存储文章 ID
    return existing_data

# 写入 CSV 文件
def writerRow(row, existing_data):
    file_path = os.path.join(script_dir, 'articleData.csv')  # 使用绝对路径
    if row[0] not in existing_data:  # 检查是否已经存在
        with open(file_path, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

# 获取微博数据
def getCommentsData(url, params):
    headers = {
        'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWm2Y1HFfkWlN0PLpZ_MOoT5JpX5KMhUgL.Fo-71heESheRS0B2dJLoI7DVwg_awg8X9g44; SINAGLOBAL=5508538758124.011.1735751090248; UOR=,,cn.bing.com; ULV=1738242752487:32:6:2:4009111466137.5938.1738242752443:1738053062851; XSRF-TOKEN=TUmE-L-IcFAR8Xfv7ZWuIaHY; ALF=1742557673; SUB=_2A25KsbS5DeRhGeNO41ET9C3EzDiIHXVpz0hxrDV8PUJbkNANLRnRkW1NTttMbpJhxDwT8klnHKxHrARZqVStFOyf; WBPSESS=0Hgcmu6MbMQzjQhdRMoliXGk8m6TOWklOqsGzR49K-zLt54XcQhBnjh1BUEMe9ws44uSIzVp2RcAWc0HBi6QcvWl2oJ2w90oP_eXV2IQ4aVxKSmVJtURUo-Aq1nljLUJMlf9058KsDPWy_4Sgj-GhQ==',
        # 替换为你的 Cookie
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        time.sleep(random.uniform(1, 3))  # 随机延迟 1-3 秒
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('statuses', [])
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"请求异常1：{e}")
        return []

# 获取长文本内容
def fetch_long_text(mblog_id):
    url = f"https://weibo.com/ajax/statuses/longtext?id={mblog_id}"  # 长文本 API
    headers = {
        'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWm2Y1HFfkWlN0PLpZ_MOoT5JpX5KMhUgL.Fo-71heESheRS0B2dJLoI7DVwg_awg8X9g44; SINAGLOBAL=5508538758124.011.1735751090248; UOR=,,cn.bing.com; ULV=1738242752487:32:6:2:4009111466137.5938.1738242752443:1738053062851; XSRF-TOKEN=TUmE-L-IcFAR8Xfv7ZWuIaHY; ALF=1742557673; SUB=_2A25KsbS5DeRhGeNO41ET9C3EzDiIHXVpz0hxrDV8PUJbkNANLRnRkW1NTttMbpJhxDwT8klnHKxHrARZqVStFOyf; WBPSESS=0Hgcmu6MbMQzjQhdRMoliXGk8m6TOWklOqsGzR49K-zLt54XcQhBnjh1BUEMe9ws44uSIzVp2RcAWc0HBi6QcvWl2oJ2w90oP_eXV2IQ4aVxKSmVJtURUo-Aq1nljLUJMlf9058KsDPWy_4Sgj-GhQ==',
        # 替换为你的 Cookie
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            long_text_data = response.json()
            return long_text_data.get('data', {}).get('longTextContent', None)
        else:
            print(f"获取长文本失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"获取长文本异常：{e}")
    return None

# 解析 JSON 数据
def parse_json(response, existing_data, group_name):
    for article in response:
        try:
            id = article['id']
            likeNum = article.get('attitudes_count', 0)
            commentsNum = article.get('comments_count', 0)
            reportsNum = article.get('reposts_count', 0)
            region = article.get('region_name', '').replace('发布于 ', '') or '无'
            content = article.get('text_raw', '')  # 默认获取内容
            contentLength = article.get('textLength', len(content))
            createdAt = datetime.strptime(article['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
            detailUrl = f"https://weibo.com/{id}/{article.get('mblogid', '')}"
            authorAvatar = article['user'].get('avatar_large', '')
            authorName = article['user'].get('screen_name', '')
            authorDetail = f"https://weibo.com/u/{article['user']['id']}"
            isVip = article['user'].get('v_plus', False)

            # 如果是长文本，则获取完整内容
            if article.get('isLongText', False):
                full_content = fetch_long_text(article['id'])
                if full_content:
                    content = full_content

            writerRow([
                id, likeNum, commentsNum, reportsNum, region, content, contentLength,
                createdAt, group_name, detailUrl, authorAvatar, authorName, authorDetail, isVip
            ], existing_data)
        except Exception as e:
            print(f"解析异常2：{e}")

# 获取导航类型列表
def getAllTypeList():
    file_path = os.path.join(script_dir, 'navData.csv')  # 使用绝对路径
    typeList = []
    with open(file_path, 'r', encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            typeList.append(nav)
    return typeList

# 爬取主函数
def start(typeNum=None, pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeList = getAllTypeList()
    existingData = load_existing_data()

    # 如果 typeNum 为 None，则爬取所有分组
    if typeNum is None:
        groups_to_crawl = typeList  # 爬取所有分组
    else:
        # 如果 typeNum 有值，则只爬取指定的分组
        if typeNum < 0 or typeNum >= len(typeList):
            print(f"分组编号 {typeNum} 无效，有效范围为 0 到 {len(typeList) - 1}")
            return
        groups_to_crawl = [typeList[typeNum]]  # 只爬取指定的分组

    # 遍历需要爬取的分组
    for type_item in groups_to_crawl:
        group_name, group_id, container_id = type_item
        print(f"正在爬取分组：{group_name}")

        # 分页爬取
        for page in range(1, pageNum + 1):
            print(f"正在爬取第 {page} 页")
            params = {
                'group_id': group_id,
                'containerid': container_id,
                'max_id': page,
                'count': 10,  # 每次请求返回 10 条数据
                'extparam': 'discover|new_feed'
            }
            response = getCommentsData(articleUrl, params)
            parse_json(response, existingData, group_name)


if __name__ == '__main__':
    start()