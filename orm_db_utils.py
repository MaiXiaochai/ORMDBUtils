# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : orm_db_utils.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2021/6/24 16:05
------------------------------------------
"""
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import SingletonThreadPool


def session_manager(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        self.session = self.get_session()
        value = f(self, *args, **kwargs)
        self.session.close()

        return value

    return inner


class ORMDBUtils:
    def __init__(self, db_uri, pool_size=2, max_overflow=2, pool_timeout=-1, pool_recycle=-1):
        engine = self.__get_engine(db_uri, pool_size, max_overflow, pool_timeout, pool_recycle)
        session_factory = sessionmaker(bind=engine)
        self.session_safe = scoped_session(session_factory)
        self.session = None

    @staticmethod
    def __get_engine(db_uri, pool_size, max_overflow, pool_timeout, pool_recycle):
        _engine = None
        if "sqlite" in db_uri.lower():
            _engine = create_engine(
                db_uri,
                poolclass=SingletonThreadPool,
                connect_args={'check_same_thread': False}
            )

        else:
            _engine = create_engine(
                db_uri,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_recycle=pool_recycle
            )

        return _engine

    def get_session(self):
        return self.session_safe()

    @sessionmaker
    def fetchall(self, sql):
        rows = self.session.execute(sql)
        return rows.fetchall()

    @sessionmaker
    def fetchone(self, sql):
        row = self.session.execute(sql)
        return row.fetchone()

    @sessionmaker
    def other_method(self):
        # session_manager对self.session的获取和关闭进行了管理，所以，可以根据具体的Model对象和业务，编写特定的抽象方法
        pass
