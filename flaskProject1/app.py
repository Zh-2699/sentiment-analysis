"""
app.py
"""
import json
import logging
import sys
from threading import Thread

from docutils.nodes import comment
from flask import Flask, jsonify
import csv
from flask_cors import CORS
from flask import request
import requests
from sqlalchemy import desc

from spiders.spiderContent import start, load_existing_data, init, getAllTypeList
from database.config import Config
from database.article_comment import Article, Comment, db
from spiders.main import main


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

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

    # 查询文章数据
    query = Article.query

    # 如果传递了分组参数，则过滤结果
    if selected_group:
        query = query.filter(Article.type == selected_group)

    # 查询所有匹配的文章数据
    articles = query.all()

    for article in articles:
        article_data.append({
            'id': article.id,
            'likeNum': article.likeNum,
            'commentNum': article.commentsNum,
            'repostsNum': article.reportsNum,
            'region': article.region,
            'content': article.content,
            'contentLength': article.contentLength,
            'createdAt': article.createdAt,
            'type': article.type,
            'detailUrl': article.detailUrl,
            'authorAvatar': article.authorAvatar,
            'authorName': article.authorName,
            'authorDetail': article.authorDetail,
            'isVip': article.isVip,
        })

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
            return jsonify({'success': False, 'message': "未传递分组信息"}), 400

        # 定义后台任务
        def backGroundTask(group):
            try:
                existingData = load_existing_data()
                group_index = None
                typeList = getAllTypeList()
                for i, item in enumerate(typeList):
                    if item[0] == group:
                        group_index = i
                        break
                print(f"group_index: {group_index}")
                if group_index is not None:
                    main(typenum=group_index, pagenum=2)
                    logging.info(f"爬虫任务完成：{group}")
                else:
                    logging.error(f"未找到分组：{group}")
            except Exception as e:
                logging.error(f"爬虫任务失败：{e}", exc_info=True)

        thread = Thread(target=backGroundTask, args=(selected_group,))
        thread.start()

        return jsonify({'success': True, 'message': '爬虫任务已启动'}), 200
    except Exception as e:
        logging.error(f"启动爬虫任务失败：{e}", exc_info=True)
        return jsonify({'success': False, 'message': '爬虫任务启动失败'}), 500

#根据id获取所有评论
@app.route('/getcommentsById', methods=['POST'])
def get_comments_by_id():
    try:
        data = request.get_json() #获取文章id
        print(f"Request data: {data}")  # 打印请求体中的数据，确保 articleId 被正确传递
        articleId = data.get('articleId')

        if not articleId:
            return jsonify({'success': False,'message':"未传递文章id"}), 400

        #查询数据库
        comments = Comment.query.filter_by(articleId=articleId).all()
        # 格式化数据
        comment_data = [{
            'articleId': comment.articleId,
            'created_at': comment.created_at,
            'likes_counts': comment.likes_counts,
            'region': comment.region,
            'content': comment.content,
            'author_name': comment.authorName,
            'author_gender': comment.authorGender,
            'author_address': comment.authorAddress,
            'author_avatar': comment.authorAvatar,
        } for comment in comments]

        return jsonify({'success': True, 'comment_data': comment_data})

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

#获取所有评论
@app.route('/getcomments', methods=['POST'])
def get_comments():
    try:
        data = request.get_json()
        print(f"Request data: {data}")

        page = data.get('page')
        per_page = 15 #先写死

        #查询数据库
        comments = Comment.query.order_by(desc(Comment.created_at)).paginate(page=page, per_page=per_page, error_out=False)

        # 格式化数据
        comment_data = [{
            'articleId': comment.articleId,
            'created_at': comment.created_at,
            'likes_counts': comment.likes_counts,
            'region': comment.region,
            'content': comment.content,
            'author_name': comment.authorName,
            'author_gender': comment.authorGender,
            'author_address': comment.authorAddress,
            'author_avatar': comment.authorAvatar,
        } for comment in comments]
        return jsonify({
            'success': True,
            'comment_data': comment_data,
            'total_comments': comments.total,
            'current_page': comments.page,
            'per_page': comments.per_page,
            'total_pages': comments.pages,
        })
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

#根据文章id获取文章
@app.route('/getArticleById', methods=['GET'])
def get_article_by_id():
    try:
        # 从请求参数中获取文章 ID
        article_id = request.args.get('id')
        if not article_id:
            return jsonify({"success": False, "message": "未传递文章 ID"}), 400

        # 查询数据库获取文章
        article = Article.query.filter_by(id=article_id).first()
        if article:
            # 格式化文章数据
            article_data = {
                'id': article.id,
                'authorName': article.authorName,
                'content': article.content,
                'likeNum': article.likeNum,
                'commentNum': article.commentsNum,
                'repostsNum': article.reportsNum,
                'region': article.region,
                'contentLength': article.contentLength,
                'createdAt': article.createdAt,
                'type': article.type,
                'detailUrl': article.detailUrl,
                'authorAvatar': article.authorAvatar,
                'authorDetail': article.authorDetail,
                'isVip': article.isVip,
            }
            return jsonify({"success": True, "article": article_data})
        else:
            return jsonify({"success": False, "message": "文章未找到"}), 404

    except Exception as e:
        # 捕获异常并返回错误信息
        print(f"Exception: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
