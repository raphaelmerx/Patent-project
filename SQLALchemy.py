from sqlalchemy import *

db = create_engine('mysql://uspto:ferrisbueller@patent.czb2hytpd5lf.us-west-1.rds.amazonaws.com:3306/uspto')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
