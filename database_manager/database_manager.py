#!/usr/binenv python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, create_engine
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

from database_manager import RecordOpratorType
BaseModel = declarative_base()

class AppInfo(BaseModel):
    __tablename__ = "appinfo"
    id = Column(TEXT(), primary_key=True)
    name = Column(TEXT(), nullable=False)
    rights = Column(TEXT(), nullable=False)
    imageurl = Column(TEXT(), nullable=False)
    artist = Column(TEXT(), nullable=False)
    title = Column(TEXT(), nullable=False)
    newestversion = Column(TEXT(), nullable=False)
    averageUserRating = Column(TEXT(), nullable=False)
    type = Column(TEXT(), nullable=False)

class Comments(BaseModel):
    __tablename__ = "comments"

    id = Column(TEXT(), primary_key=True)
    author = Column(TEXT(), nullable=False)
    version = Column(TEXT(), nullable=False)
    rating = Column(INT(), nullable=False)
    title = Column(TEXT(), nullable=False)
    content = Column(TEXT(), nullable=False)
    contenttype = Column(TEXT(), nullable=False)
    appid = Column(TEXT(), nullable=False)
    countryorarea = Column(TEXT(), nullable=False)
    createtimestamp = Column(TEXT())
    updatetimestamp = Column(TEXT())

    def __str__(self):
        return "Comment:" + self.id + " " + self.author + " " + self.title + " " + str(self.createtimestamp)

class DataManager(object):
    def __init__(self):
        #print("DataManager __init__")
        self.engine = create_engine('sqlite:///comments.db', encoding='utf-8', echo=False)
        BaseModel.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def recordCount(self):
        return len(self.session.query(Comments).all())

    #
    def addOrUpdateComment(self, comment):
        try:
            result = self.session.query(Comments).filter_by(id=comment.id).all()
            #print("->>>>>>>>>>>>>", len(result), comment.id)
            if 0 == len(result):
                self.session.add(comment)
                self.session.commit()
                print("添加新的评论:", comment.id, '/', comment.title, '/', comment.appid
                      )
                return RecordOpratorType.Insert
            else:
                #print("已存在的评论:", comment.id)
                return RecordOpratorType.Update
        except Exception as e:
            #self.session.rollback()
            print('Failed to addOrUpdateComments:', e)
            return RecordOpratorType.Error

    def addOrUpdateAppInfo(self, appinfo):
        try:
            result = self.session.query(AppInfo).filter_by(id=appinfo.id).all()
            # print("->>>>>>>>>>>>>", len(result), comment.id)
            if 0 == len(result):
                self.session.add(appinfo)
                self.session.commit()
                print("添加新的App信息:", appinfo.id, '/', appinfo.title, '/', appinfo.type)
                return RecordOpratorType.Insert
            else:
                app = self.session.query(AppInfo).get(appinfo.id)
                app = appinfo
                self.session.commit()
                print("更新App信息", appinfo.id, '/', appinfo.title, '/', appinfo.title)
                return RecordOpratorType.Update
        except Exception as e:
            # self.session.rollback()
            print('Failed to addOrUpdateAppInfo:', e)
            return RecordOpratorType.Error