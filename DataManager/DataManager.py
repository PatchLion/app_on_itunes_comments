#!/usr/binenv python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
BaseModel = declarative_base()

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

class DataManager(object):
    def __init__(self):
        print("DataManager __init__")
        self.engine = create_engine('sqlite:///comments.db', encoding='utf-8', echo=False)
        BaseModel.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def recordCount(self):
        return len(self.session.query(Comments).all())

    def addOrUpdateComments(self, comments):
        try:
            for c in comments:
                exist_lists = self.session.query(Comments).filter_by(id=c.id).all()
                if len(exist_lists) == 0:
                    print('Add comment to DB:', c.id, c.countryorarea, c.appid)
                    self.session.add(c)
                    self.session.commit()
                else:
                    print("comment ", c.id, "exist!!!")

        except Exception as e:
            #self.session.rollback()
            print('Failed to addOrUpdateComments:', e)

    def addOrUpdateComment(self, comment):
        print('comment:', comment.id)
        try:
            result = self.session.query(Comments, comment.id).all()
            if 0 == len(result):
                self.session.add(comment)
                self.session.commit()
        except Exception as e:
            #self.session.rollback()
            print('Failed to addOrUpdateComments:', e)