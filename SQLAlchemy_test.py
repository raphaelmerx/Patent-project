from sqlalchemy import *
engine = create_engine('sqlite:///:memory:', echo=False)

'''
# create MetaData
metadata = MetaData()
# new table users_table
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(50)),
                    Column('fullname', String(50)),
                    Column('password', String(50))
                    )
metadata.create_all(engine)
'''

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# defining the User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
        
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
Base.metadata.create_all(engine)

# linking users_table to User ????
users_table = User.__table__

# create a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# add a new user
ed_user = User('ed', 'Ed Jones', 'edspassword')
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first() 
our_user

'''
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(50)),
                    Column('fullname', String(50)),
                    Column('password', String(50))
                    )
metadata.create_all(engine) 

class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

from sqlalchemy.orm import mapper
mapper(User, users_table) 
'''
