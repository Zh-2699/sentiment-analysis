""""
article_comment.py
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
class Article(db.Model):
    __tablename__ = 'articles'  # 表名

    id = db.Column(db.Integer, primary_key=True)   # 文章id
    likeNum = db.Column(db.BigInteger)             # 点赞数
    commentsNum = db.Column(db.BigInteger)         # 评论数
    reportsNum = db.Column(db.BigInteger)          # 转发数
    region = db.Column(db.String(255))             # 区域
    content = db.Column(db.Text)                   # 内容
    contentLength = db.Column(db.BigInteger)       # 内容长度
    createdAt = db.Column(db.String(255))          # 创建时间
    type = db.Column(db.String(255))               # 类型
    detailUrl = db.Column(db.String(255))          # 详情页
    authorAvatar = db.Column(db.String(255))       # 作者头像
    authorName = db.Column(db.String(255))         # 作者名字
    authorDetail = db.Column(db.String(255))       # 作者详情页
    isVip = db.Column(db.Boolean)                  # 是否是vip   1是 0否

    comments = db.relationship('Comment', backref='article_ref', lazy=True)

    def __repr__(self):
        return f'<Article {self.id}>'

class Comment(db.Model):
    __tablename__ = 'comments'  # 表名
    articleId = db.Column(db.BigInteger, db.ForeignKey('articles.id'), nullable=False, primary_key=True)  # 文章id
    created_at = db.Column(db.String(255))      # 创建时间
    likes_counts = db.Column(db.BigInteger)         # 点赞数
    region = db.Column(db.String(255))          # 区域
    content = db.Column(db.Text, primary_key=True)                # 内容
    authorName = db.Column(db.String(255))      # 作者名字
    authorGender = db.Column(db.String(255))    # 作者性别
    authorAddress = db.Column(db.String(255))   # 作者地址
    authorAvatar = db.Column(db.String(255))    # 作者头像


    def __repr__(self):
        return f'<Comment {self.articleId} on Article {self.content[:20]}>'

