#!/usr/binenv python
# -*- coding: utf-8 -*-
from comments import db_session, BaseModel, RecordExistType
from sqlalchemy import Column
from sqlalchemy.types import *
from mylogging import mylogger

class Comments(BaseModel):
    __tablename__ = "comments"
    id = Column(TEXT(), primary_key=True)
    author = Column(TEXT(), nullable=False)
    version = Column(TEXT(), nullable=False)
    rating = Column(INT(), nullable=False)
    title = Column(TEXT(), nullable=False)
    content = Column(TEXT(), nullable=False)
    content_type = Column(TEXT(), nullable=False)
    app_id = Column(TEXT(), nullable=False)
    country_or_area = Column(TEXT(), nullable=False)
    create_timestamp = Column(INTEGER())
    update_timestamp = Column(INTEGER())

    @classmethod
    def is_comments_exist(cls, comment_id):
        try:
            result = db_session.query(Comments).filter_by(id=comment_id).all()
            if(0 != len(result)):
                return RecordExistType.Exist
            else:
                return RecordExistType.NotExist
        except Exception as e:
            mylogger.ERROR("Comments.is_comments_exist:", e)
            return RecordExistType.Error

    @classmethod
    def add_comments(cls, comment_item):
        mylogger.info("Insert item:", comment_item["id"], comment_item["title"]);
        new_comment = Comments()
        new_comment.id = comment_item["id"]
        new_comment.author = comment_item["author"]
        new_comment.version = comment_item["version"]
        new_comment.rating = comment_item["rating"]
        new_comment.title = comment_item["title"]
        new_comment.content = comment_item["content"]
        new_comment.country_or_area = comment_item["country_or_area"]
        new_comment.app_id = comment_item["app_id"]
        new_comment.content_type = comment_item["content_type"]
        new_comment.create_timestamp = comment_item["create_timestamp"]
        new_comment.update_timestamp = comment_item["update_timestamp"]
        try:
            db_session.add(new_comment)
            db_session.commit()
        except Exception as e:
            mylogger.error("Comments.add_comments:", e)

    @classmethod
    def requry_record_after_timestamp(cls, last_timestamp):
        result = db_session.query(Comments).filter(Comments.update_timestamp > last_timestamp).all()
        return result