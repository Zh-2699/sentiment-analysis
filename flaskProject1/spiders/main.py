import io
import os
import sys

import pandas as pd
from sqlalchemy import create_engine, exc
from spiders.spiderComments import start as spiderCommentsStart
from spiders.spiderContent import start as spiderContentStart
from contextlib import contextmanager

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 设置文件路径
article_data_path = os.path.join(current_dir, 'articleData.csv')
article_comments_path = os.path.join(current_dir, 'articleComments.csv')

# 创建数据库连接
engine = create_engine('mysql://root:1234@localhost/weiboarticles?charset=utf8mb4')

# 使用上下文管理器来管理数据库事务
@contextmanager
def transaction_session(engine):
    """数据库事务管理器，确保提交或回滚"""
    connection = engine.connect()
    transaction = connection.begin()  # 开始事务
    try:
        yield connection
        transaction.commit()  # 提交事务
    except exc.SQLAlchemyError as e:
        transaction.rollback()  # 回滚事务
        print(f"数据库操作失败，事务已回滚: {e}")
        raise  # 重新抛出异常以便进一步处理
    finally:
        connection.close()

def save_to_database():
    # 修改标准输出的编码为 utf-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    try:
        # 从数据库读取已有数据
        articleOldPd = pd.read_sql('SELECT id FROM articles', con=engine)
        commentsOldPd = pd.read_sql('SELECT articleId FROM comments', con=engine)

        # 从 CSV 文件读取新数据
        articleNewPd = pd.read_csv(article_data_path)
        commentsNewPd = pd.read_csv(article_comments_path)

        # 过滤掉数据库中已存在的文章和评论
        articleNewPd = articleNewPd[~articleNewPd['id'].isin(articleOldPd['id'])]
        commentsNewPd = commentsNewPd[~commentsNewPd['articleId'].isin(commentsOldPd['articleId'])]

        # 使用事务进行数据插入
        with transaction_session(engine) as connection:
            # 将新数据写入数据库
            if not articleNewPd.empty:
                articleNewPd.to_sql('articles', con=connection, if_exists='append', index=False)
                print(f"成功插入 {len(articleNewPd)} 条文章数据")
            else:
                print("没有新的文章数据需要插入")

            if not commentsNewPd.empty:
                commentsNewPd.to_sql('comments', con=connection, if_exists='append', index=False)
                print(f"成功插入 {len(commentsNewPd)} 条评论数据")
            else:
                print("没有新的评论数据需要插入")

    except Exception as e:
        print(f"处理异常：{e}")

def remove_files():
    """删除已处理的 CSV 文件"""
    try:
        os.remove(article_data_path)
        os.remove(article_comments_path)
        print("CSV 文件已删除")
    except Exception as e:
        print(f"删除文件失败: {e}")

def main(typenum=None, pagenum=2):
    print('main 函数被调用')
    print('文章正在爬取...')
    spiderContentStart(typenum, pagenum)
    print('评论正在爬取...')
    spiderCommentsStart()
    print('数据正在保存...')
    save_to_database()
    remove_files()

if __name__ == '__main__':
    main()
