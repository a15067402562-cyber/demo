import pymysql
from dbutils.pooled_db import PooledDB

POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,   ##初始最少创建空闲的连接
    maxcached=5,   ##最多空闲的连接数
    blocking=True,
    setsession=[],
    ping=0,
    host="127.0.0.1",port=3306,user="root",password="root",db="flask_study",charset="utf8"
)
from pymysql import cursors

def fetch_one(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql,params)
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def fetch_all(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql,params)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def idu(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql,params)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

