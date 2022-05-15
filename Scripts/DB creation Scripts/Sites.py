# %%
import sqlalchemy as db
from sqlalchemy import Column, BigInteger, String, create_engine, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# %%
engine = create_engine('mysql+pymysql://root:Welcome1@localhost:3306/jobs')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


# %%
class Site(Base):
    __tablename__ = 'sites'

    link = Column(String(200), primary_key=True)
    title = Column(String(50))
    location = Column(String(50))
    codeBase = Column(String(10))
    state = Column(String(50))
    descriptionRequired = Column(Boolean)

# %%
Base.metadata.create_all() 


