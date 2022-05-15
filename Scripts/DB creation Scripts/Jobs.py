# %%
import sqlalchemy as db
from sqlalchemy import Column, BigInteger, String, create_engine, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# %%
engine = create_engine('mysql+pymysql://root:Welcome1@localhost:3306/jobs')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


# %%
class Job(Base):
    __tablename__ = 'jobs'

    jobid = Column(BigInteger, primary_key=True)
    link = Column(String(200), primary_key=True)
    title = Column(String(300))
    department = Column(String(100))
    jobNumber = Column(String(50),nullable=True)
    salaryRange = Column(String(100),nullable=True)
    jobType = Column(String(50),nullable=True)
    location = Column(String(100),nullable=True)
    state = Column(String(25),nullable=True)
    description = Column(Text,nullable=True)
    startDate = Column(DateTime,nullable=True)
    pubDate = Column(DateTime)
    closeDate = Column(DateTime,nullable=True)
    
    def __init__(self, startDate, pubDate, closeDate, jobid, link, title, department, jobNumber, salaryRange, jobType, location, state, description):
        self.jobid = jobid
        self.link = link
        self.title = title
        self.department = department
        self.jobNumber = jobNumber
        self.salaryRange = salaryRange
        self.jobType=jobType
        self.location=location
        self.state=state
        self.description=description
        self.startDate=startDate
        self.pubDate=pubDate
        self.closeDate=closeDate

# %%
Base.metadata.create_all() 


