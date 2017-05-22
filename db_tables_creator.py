#!/usr/binenv python
# -*- coding: utf-8 -*-
from comments import db_engine, BaseModel
from db_tables import *

BaseModel.metadata.create_all(db_engine)