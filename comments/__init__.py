from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum
from scrapy.utils.log import configure_logging

class RecordExistType(Enum):
    NotExist = 0
    Exist = 1
    Error = 2

def read_html(file):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    return html

configure_logging(install_root_handler=False)
BaseModel = declarative_base()
db_engine = create_engine('sqlite:///comments.db', encoding='utf-8', echo=False)
DBSession = sessionmaker(bind=db_engine)
db_session = DBSession()
template_table_data = read_html('template_table.html')
template_row_data = read_html('template_row.html')
