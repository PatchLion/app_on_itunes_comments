#!/usr/binenv python
# -*- coding: utf-8 -*-
from comments import db_session, BaseModel, RecordExistType
from sqlalchemy import Column
from sqlalchemy.types import *
from sqlalchemy.sql import and_
from mylogging import mylogger

class Comments(BaseModel):
    __tablename__ = "comments"
    id = Column(TEXT(), primary_key=True)
    author = Column(TEXT(), nullable=False)
    version = Column(TEXT(), nullable=False)
    rating = Column(INT(), nullable=False)
    title = Column(TEXT(), nullable=False)
    content = Column(TEXT(), nullable=False)
    content_trans_cn = Column(TEXT(), nullable=True)
    content_trans_en = Column(TEXT(), nullable=True)
    content_type = Column(TEXT(), nullable=False)
    app_id = Column(TEXT(), nullable=False)
    country_or_area = Column(TEXT(), nullable=False)
    create_timestamp = Column(INTEGER())
    update_timestamp = Column(INTEGER())

    @classmethod
    def is_comments_exist(cls, comment_id):
        try:
            result = db_session.query(Comments).filter(Comments.id==comment_id).all()
            if(0 != len(result)):
                return RecordExistType.Exist
            else:
                return RecordExistType.NotExist
        except Exception as e:
            mylogger.error("Comments.is_comments_exist: {0}".format(str(e)))
            return RecordExistType.Error

    @classmethod
    def add_comments(cls, comment_item):
        mylogger.info("Insert item: {0} {1}".format(comment_item["id"], comment_item["title"]))
        new_comment = Comments()
        new_comment.id = comment_item["id"]
        new_comment.author = comment_item["author"]
        new_comment.version = comment_item["version"]
        new_comment.rating = comment_item["rating"]
        new_comment.title = comment_item["title"]
        new_comment.content = comment_item["content"]
        new_comment.content_trans_cn = comment_item["content_trans_cn"]
        new_comment.content_trans_en = comment_item["content_trans_en"]
        new_comment.country_or_area = comment_item["country_or_area"]
        new_comment.app_id = comment_item["app_id"]
        new_comment.content_type = comment_item["content_type"]
        new_comment.create_timestamp = comment_item["create_timestamp"]
        new_comment.update_timestamp = comment_item["update_timestamp"]
        try:
            db_session.add(new_comment)
            db_session.commit()
        except Exception as e:
            mylogger.error("Comments.add_comments: {0}".format(e))

    @classmethod
    def requry_record_after_timestamp(cls, appid, last_timestamp):
        result = db_session.query(Comments).filter(and_(Comments.update_timestamp > last_timestamp, Comments.app_id == appid)).all()
        return result

    @classmethod
    def requery_not_translate_comments(cls, skips=[], exps = ["cn", "tw"]):
        conds = [(Comments.country_or_area != lan) for lan in exps]
        conds.append(Comments.content_trans_cn == "")
        skip_conds = [(Comments.content != content) for content in skips]
        result = db_session.query(Comments).filter(and_(*conds, *skip_conds)).order_by(Comments.create_timestamp, Comments.version).all()
        return result

    @classmethod
    def update_translate_comment(cls, old, tran):
        db_session.query(Comments).filter(Comments.content == old).update({Comments.content_trans_cn: tran})
        db_session.commit()

    @classmethod
    def update_translate_comments(cls, mapdata):
        olds = mapdata.keys()
        conds = [(Comments.content == key) for key in olds]
        results = db_session.query(Comments).filter(*conds).all()

        for result in results:
            #mylogger.info("update_translate_comment:", result.content, "-->", mapdata[result.content])
            result.content_trans_cn = mapdata[result.content]

        db_session.commit()
