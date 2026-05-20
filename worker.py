"""
去队列中获取任务，执行并写入到结果队列
"""
import hashlib
import json

import redis

REDIS_CONN_PARAMS={
        "host":"127.0.0.1",
        "port":6379,
        "encoding":"utf-8",
    }
REDIS_POOL=redis.ConnectionPool(**REDIS_CONN_PARAMS)
TASK_QUEUE="spider_task_list"
RESULT_QUEUE="spider_result_list"


def get_task():
    conn = redis.Redis(connection_pool=REDIS_POOL)
    data=conn.brpop(TASK_QUEUE,timeout=10)     #阻塞弹出,超时时间为10s,返回None
    if not data:
        return
    return json.loads(data[1].decode("utf-8"))

def set_result(tid,value):
    conn = redis.Redis(connection_pool=REDIS_POOL)
    conn.hset(RESULT_QUEUE,tid,value)

def run():
    while True:
        # 1.获取任务
        task_dict=get_task()
        print(task_dict)
        if not task_dict:
            continue

        # 2.执行耗时操作
        ordered_string=task_dict["data"]
        encrypt_string = ordered_string + "74d89af48b654c8864d997da"
        obj = hashlib.md5(encrypt_string.encode("utf-8"))
        sign = obj.hexdigest()

        tid=task_dict["tid"]
        set_result(tid,sign)

if __name__ == '__main__':
    run()