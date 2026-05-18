import redis
import pymysql
from dbutils.pooled_db import PooledDB
from concurrent.futures import ThreadPoolExecutor

DB_POOL = PooledDB(
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


def fetch_all(sql,params):
    conn=DB_POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql,params)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_one(sql,params):
    conn=DB_POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql,params)
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def db_update(sql,params):
    conn=DB_POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql,params)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

POOL=redis.connection.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8',max_connections=100)

def pop_queue():
    conn=redis.Redis(connection_pool=POOL)
    data=conn.brpop("Flask_Task_Queue",timeout=10)
    if not data:
        return
    return data[1].decode("utf-8")


def db_queue_init():
    """
    1、去数据库获取待执行的订单ID
    2、去redis中获取待执行的订单ID
    3、找到数据库中有且redis队列中没有的订单ID -> 重新放到redis队列
    """
    db_list=fetch_all("select id from `order` where status=1",[])
    db_id_list={item['id'] for item in db_list}

    conn=redis.Redis(connection_pool=POOL)
    total_count=conn.llen("Flask_Task_Queue")
    cache_list=conn.lrange("Flask_Task_Queue",0,total_count)
    cache_int_list={int(item.decode("utf-8")) for item in cache_list}

    need_push=db_id_list - cache_int_list
    if need_push:
        conn.lpush("Flask_Task_Queue",*need_push)

def get_order_object(order_id):
    res=fetch_one("select * from `order` where id=%s",[order_id])
    return res

def update_order(order_id,status):
    db_update("update `order` set status=%s where id=%s",[status,order_id])

def delete_order(order_id):
    db_update("delete from `order` where id=%s",[order_id])

def task(info_dict):
    pass


def run():
    #1、初始化数据库未在队列中的订单
    db_queue_init()
    while True:
        #2、去队列中获取订单
        order_id=pop_queue()
        if not order_id:
            continue
        #3、订单是否存在
        order_dict=get_order_object(order_id)
        if not order_dict:
            continue
        #4、更新订单状态
        update_order(order_id,2)
        #5、执行订单
        print("执行订单任务：",order_dict)
        thread_pool = ThreadPoolExecutor(10)
        for i in range(order_dict["count"]):
            thread_pool.submit(task, order_dict)
        thread_pool.shutdown()
        #6、执行完成
        update_order(order_id,3)

if __name__ == '__main__':
    run()