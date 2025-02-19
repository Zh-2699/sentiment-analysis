''''
spiderComments.py
'''
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
    file_path = os.path.join(script_dir, 'articleComments.csv')  # 使用绝对路径
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'articleId', 'created_at', 'likes_counts', 'region', 'content',
                'authorName', 'authorGender', 'authorAddress', 'authorAvatar',
            ])


# 加载已存在的数据
def load_existing_data():
    file_path = os.path.join(script_dir, 'articleComments.csv')  # 使用绝对路径
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
    file_path = os.path.join(script_dir, 'articleComments.csv')  # 使用绝对路径
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
            return response.json().get('data', [])
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"article请求异常1：{e}")
        return []


# 获取长文本内容
def fetch_long_text(mblog_id):
    url = f"https://weibo.com/ajax/statuses/longtext?id={mblog_id}"  # 长文本 API
    headers = {
        'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWm2Y1HFfkWlN0PLpZ_MOoT5JpX5KMhUgL.Fo-71heESheRS0B2dJLoI7DVwg_awg8X9g44; SINAGLOBAL=5508538758124.011.1735751090248; ULV=1736492224385:29:3:2:2445340372437.9253.1736492224286:1736330635505; XSRF-TOKEN=otVBp6IWWOX0l-zOxk8zbU8o; ALF=1739854460; SUB=_2A25KiPUsDeRhGeNO41ET9C3EzDiIHXVp5AjkrDV8PUJbkNANLUfnkW1NTttMbibjXFn0DnNIGjBn9OGZDV5JP7Gz; WBPSESS=0Hgcmu6MbMQzjQhdRMoliXGk8m6TOWklOqsGzR49K-zUspmopQhvzUSpXDDtw2ZZ63JZermirOz1Ak_DLWD3ESYSIq1WG6f1mTz2-RojUU0aFgWsl9qv7lDFwQvUW19lmCk01A0GddVHx3A5xPMihw==',
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
        print(f"获取长文本异常2：{e}")
    return None


#获取文章详情
def get_article_details(mblog_id):
    url = f'https://weibo.com/ajax/statuses/show?id={str(mblog_id)}'
    headers = {
        'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWm2Y1HFfkWlN0PLpZ_MOoT5JpX5KMhUgL.Fo-71heESheRS0B2dJLoI7DVwg_awg8X9g44; SINAGLOBAL=5508538758124.011.1735751090248; UOR=,,cn.bing.com; ULV=1738242752487:32:6:2:4009111466137.5938.1738242752443:1738053062851; XSRF-TOKEN=TUmE-L-IcFAR8Xfv7ZWuIaHY; ALF=1742557673; SUB=_2A25KsbS5DeRhGeNO41ET9C3EzDiIHXVpz0hxrDV8PUJbkNANLRnRkW1NTttMbpJhxDwT8klnHKxHrARZqVStFOyf; WBPSESS=0Hgcmu6MbMQzjQhdRMoliXGk8m6TOWklOqsGzR49K-zLt54XcQhBnjh1BUEMe9ws44uSIzVp2RcAWc0HBi6QcvWl2oJ2w90oP_eXV2IQ4aVxKSmVJtURUo-Aq1nljLUJMlf9058KsDPWy_4Sgj-GhQ==',
        # 替换为你的 Cookie
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            article_data = response.json()
            if article_data.get('ok') == 1:  # 检查微博是否存在
                content = article_data.get('text_raw', '没有获取到文章内容')
                return content
            else:
                print(f"微博 ID {mblog_id} 不存在，错误信息: {article_data.get('message')}")
                return f"微博不存在: {article_data.get('message')}"
        else:
            print(f"获取文章内容失败，状态码：{response.status_code}")
            return f"请求失败，状态码：{response.status_code}"
    except Exception as e:
        print(f"获取文章内容异常：{e}")
        return f"请求异常3：{e}"


# 解析 JSON 数据
# 解析 JSON 数据
def parse_json(response, existing_data, articleId):
    for comment in response:
        try:
            # 打印整个评论数据，检查返回结构
            # print("评论数据:", comment)

            # 使用 .get() 方法获取数据，避免出现 KeyError
            article_id = comment.get('id', '无ID')  # 如果没有 'id'，则返回 '无ID'
            created_at = comment.get('created_at', '无时间')  # 获取评论时间
            likes_counts = comment.get('like_counts', 0)  # 获取点赞数，默认为 0
            region = comment.get('source', '未知')  # 获取来源，默认为 '未知'
            content = comment.get('text_raw', '无内容')  # 获取评论内容，如果没有返回 '无内容'
            author_name = comment.get('user', {}).get('screen_name', '无用户名')
            author_gender = comment.get('user', {}).get('gender', '未知')  # 获取性别，默认为 '未知'
            author_address = comment.get('user', {}).get('location', '未知')  # 获取用户地址，默认为 '未知'
            author_avatar = comment.get('user', {}).get('avatar_large', '无头像')  # 获取头像，默认为 '无头像'

            # 打印详细信息
            # print(f"评论 ID: {article_id}")
            # print(f"评论时间: {created_at}")
            # print(f"点赞数: {likes_counts}")
            # print(f"来源: {region}")
            # print(f"评论内容: {content}")
            # print(f"作者: {author_name}")
            # print(f"性别: {author_gender}")
            # print(f"地址: {author_address}")
            # print(f"头像: {author_avatar}")
            # print("-" * 50)

            # 将评论信息和文章信息存入 CSV 文件
            row = [
                articleId, created_at, likes_counts, region, content,
                author_name, author_gender, author_address, author_avatar
            ]
            writerRow(row, existing_data)
        except Exception as e:
            print(f"解析异常4：{e}")


# 获取导航类型列表
def getArticleList():
    file_path = os.path.join(script_dir, 'articleData.csv')  # 使用绝对路径
    articleList = []
    with open(file_path, 'r', encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            articleList.append(nav)
    return articleList


# 爬取主函数
def start(typeNum=None, pageNum=2):
    commentsUrl = 'https://weibo.com/ajax/statuses/buildComments'
    init()
    articleList = getArticleList()
    # print(articleList)
    existing_data = load_existing_data()
    for article in articleList:
        articleId = article[0]
        print('正在爬取id值为%s的文章评论' %articleId )
        time.sleep(2)
        params = {
            'id': int(articleId),
            'is_show_bulletin': 2,
        }
        response = getCommentsData(commentsUrl, params)
        parse_json(response, existing_data, articleId)



if __name__ == '__main__':
    start()
