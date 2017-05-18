from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum

class RecordExistType(Enum):
    NotExist = 0
    Exist = 1
    Error = 2

def read_html(file):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    return html

BaseModel = declarative_base()
mysettings = get_project_settings()
db_engine = create_engine('sqlite:///comments.db', encoding='utf-8', echo=False)
DBSession = sessionmaker(bind=db_engine)
db_session = DBSession()
template_table_data = read_html('template_table.html')
template_row_data = read_html('template_row.html')
