# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : example.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2021/6/25 13:46
------------------------------------------
"""
from threading import Lock

from orm_db_utils import ORMDBUtils

db_uri = "sqlite:///maixiaochai.db"
db = ORMDBUtils(db_uri)

lock = Lock()


def task(sql):
    with lock:
        data = db.fetchone(sql)
        print(data)
