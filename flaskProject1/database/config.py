"""
config.py
"""
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/weiboarticles?charset=utf8mb4'
