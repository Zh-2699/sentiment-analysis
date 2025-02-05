"""
app.py
"""
import json
import logging
import sys
from threading import Thread

from flask import Flask, jsonify
import csv
from flask_cors import CORS
from flask import request
import requests
from spiders.spiderContent import start, load_existing_data, init, getAllTypeList

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# 获取文章导航
@app.route('/article/navdata', methods=['GET'])
def get_nav_data():
    nav_data = []
    with open('spiders/navData.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nav_data.append({
                'name': row['TypeName'],
                'gid': row['gid'],
                'containerid': row['containerid'],
            })
    nav_data = {
        'groups': nav_data
    }
    return jsonify(nav_data)

# 获取文章数据
@app.route('/article/data', methods=['GET'])
def get_article_data():
    print("Accessing /article/data")
    article_data = []
    selected_group = request.args.get('group')  # 直接从URL中读取参数
    print(f"Selected group: {selected_group}")
    with open('spiders/articleData.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            article = {
                'id': row['id'],
                'likeNum': row['likeNum'],
                'commentNum': row['commentsNum'],
                'repostsNum': row['reportsNum'],
                'region': row['region'],
                'content': row['content'],
                'contentLength': row['contentLength'],
                'createdAt': row['createdAt'],
                'type': row['type'],
                'detailUrl': row['detailUrl'],
                'authorAvatar': row['authorAvatar'],
                'authorName': row['authorName'],
                'authorDetail': row['authorDetail'],
                'isVip': row['isVip'],
            }

            # 如果指定了分组（group），则进行过滤
            if not selected_group or article['type'] == selected_group:
                article_data.append(article)  # 将文章数据添加到列表中

    return jsonify(article_data)  # 返回文章数据

#获取微博热搜
@app.route('/hotSearch', methods=['GET'])
def get_hot_search():
    print("Accessing /hotSearch")
    try:
        # 请求微博热搜api
        url = 'https://weibo.com/ajax/side/hotSearch'
        response = requests.get(url)
        data = response.json()

        # 检查数据
        if data.get('ok') == 1:
            hot_search_data = data.get('data', {}).get('realtime', [])
            return jsonify(hot_search_data[:20])
        else:
            return jsonify({'error': '获取热搜失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#爬取数据
init()

@app.route('/article/crawl', methods=['POST'])
def crawl_article_data():
    try:
        # 从请求中获取参数
        data = request.get_json()
        print(data)
        selected_group = data.get('group')
        if not selected_group:
            return jsonify({'success': False, 'message':"未传递分组信息"}), 400

        #定义后台任务
        def backGroundTask(group):
            existingData = load_existing_data()
            group_index = None
            typeList = getAllTypeList()
            # print(f"typeList: {typeList}")
            for i, item in enumerate(typeList):
                if item[0] == group:
                    group_index = i
                    break
            if group_index is not None:
                start(typeNum=group_index, pageNum=2)

        thread = Thread(target=backGroundTask, args=(selected_group,))
        thread.start()

        return jsonify({'success': True, 'message':'爬虫任务已启动'}, ), 200
    except Exception as e:
        return jsonify({'success':'false', 'message':'爬虫任务失败'}), 500

if __name__ == '__main__':
    app.run(debug=True)
