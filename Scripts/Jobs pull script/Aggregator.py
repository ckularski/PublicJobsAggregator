# %%
import requests 
from bs4 import BeautifulSoup

import sqlalchemy as db
from sqlalchemy import Column, BigInteger, String, create_engine, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from datetime import datetime
import pytz

import re

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
    
    #idade = Column(Integer())

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
class Site(Base):
    __tablename__ = 'sites'

    link = Column(String(200), primary_key=True)
    title = Column(String(50))
    location = Column(String(50))
    codeBase = Column(String(10))
    state = Column(String(50))
    descriptionRequired = Column(Boolean)

# %%
sites = engine.execute(
    text(
        "SELECT * from sites where title like '%'"
    )
)

# %%
for site in sites:
    url = site.link
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content)
    jobListings=[]
    regex = re.compile(r'[\n\r\t]')
    editSalaryList = ['Depends on Qualifications', 'See Position Description', 'Not Displayed']
    if site.codeBase == 'atom':
        items = soup.findAll('entry')
        print (url+':'+str(len(items)))
        for item in items:
            jobListing = {}
            jobListing['link'] = item.id.text
            ids = item.id.text.split('/')
            jobListing['jobid']= ids[len(ids)-1]
            jobListing['pubdate'] = datetime.strptime(item.published.text, '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.UTC).replace(tzinfo=None)
            jobListing['title'] = item.title.text
            jobListing['dept'] = item.author.text.strip()
            des=item.content.text.strip()
            soupDes = BeautifulSoup(des)
            if soupDes.find('div')==None:
                jobListing['description']=soupDes
            else:
                div = soupDes.find('div')
                jobListing['description']=div.string
            if 'location' not in jobListing.values():
                jobListing['location'] = site.location
            if 'state' not in jobListing.values():
                jobListing['state'] = site.state
            if site.descriptionRequired == 0:
                jobListing['description']= ''
            jobListings.append(jobListing)
        for jobListing in jobListings:
            session = Session()
            #startDate, pubDate, closeDate, jobid, link, title, department, jobNumber, salaryRange, jobType, location, state, description
            job = Job(db.sql.null(),jobListing['pubdate'],db.sql.null(),int(jobListing['jobid']),jobListing['link'],jobListing['title'],jobListing['dept'],db.sql.null(),db.sql.null(),db.sql.null(),jobListing['location'],jobListing['state'],jobListing['description'])
            session.add(job)
            try:
                session.commit()
            except:
                session.rollback()
    if site.codeBase == 'neogov':
        items = soup.findAll('item')
        print (url+':'+str(len(items)))
        for item in items:
            jobListing = {}
            jobListing['link'] = regex.sub("", item.find(text=re.compile("https://")))
            jobListing['pubdate'] = item.pubdate.text
            jobListing['title'] = item.title.text
            jobListing['dept'] = item.find('joblisting:department').text
            jobListing['description']=item.description.text.strip()
            jobListing['jobnumber']=item.find('joblisting:jobnumbersingle').text
            jobListing['jobid']=item.find('joblisting:jobid').text
            jobListing['startdate']=item.find('joblisting:advertisefromdateutc').text
            jobListing['closedate']=item.find('joblisting:advertisetodatetimeutc').text
            currency = item.find('joblisting:salarycurrency').text
            minRange = item.find('joblisting:minimumsalary').text
            maxRange = item.find('joblisting:maximumsalary').text
            if minRange in editSalaryList:
                jobListing['salaryRange'] = minRange
            else:
                salRange = currency + ' ' + minRange 
                if maxRange and maxRange != minRange:
                    salRange += (' - '+ maxRange)
                jobListing['salaryRange']= salRange +' per '+item.find('joblisting:salaryinterval').text
            jobListing['jobtype']=item.find('joblisting:jobtype').text
            jobListing['location']=item.find('joblisting:location').text
            jobListing['state']=item.find('joblisting:state').text
            if 'location' not in jobListing.values():
                jobListing['location'] = site.location
            if 'state' not in jobListing.values():
                jobListing['state'] = site.state
            if site.descriptionRequired == 0:
                jobListing['description']= ''
            jobListings.append(jobListing)
        for jobListing in jobListings:
            session = Session()
            if(type(jobListing['startdate']) is not datetime):
                startDate=jobListing['startdate'].split(',')
                if(len(startDate)>1):
                    #print(startDate[1])
                    jobListing['startdate']=datetime.strptime(startDate[1].strip(), '%d %b %Y %H:%M:%S')
                else:
                    jobListing['startdate']=datetime.strptime(startDate[0].strip(), '%d %b %Y %H:%M:%S')
            if(jobListing['closedate']=='Continuous'):
                jobListing['closedate']=db.sql.null()
            #Fri, 15 Apr 2022 23:59:00
            else:
                closeDate=jobListing['closedate'].split(',')
                if(len(startDate)>1):
                    jobListing['closedate']=datetime.strptime(closeDate[1].strip(), '%d %b %Y %H:%M:%S')
                else:
                    jobListing['closedate']=datetime.strptime(closeDate[0].strip(), '%d %b %Y %H:%M:%S')
            #Tue, 12 Oct 2021 21:10:33 GMT
            pubDate=jobListing['pubdate'].split(',')
            if(len(startDate)>1):
                jobListing['pubdate']=datetime.strptime(pubDate[1].strip(), '%d %b %Y %H:%M:%S %Z').astimezone(pytz.UTC).replace(tzinfo=None)
            else:
                jobListing['pubdate']=datetime.strptime(pubDate[0].strip(), '%d %b %Y %H:%M:%S %Z').astimezone(pytz.UTC).replace(tzinfo=None)
            #print(jobListing['startdate'])
            job = Job(jobListing['startdate'],jobListing['pubdate'],jobListing['closedate'],int(jobListing['jobid']),jobListing['link'],jobListing['title'],jobListing['dept'],jobListing['jobnumber'],jobListing['salaryRange'],jobListing['jobtype'],jobListing['location'],jobListing['state'],jobListing['description'])
            session.add(job)
            try:
                session.commit()
            except:
                session.rollback()
    if site.codeBase == 'rss':
        items = soup.findAll('item')
        print (url+':'+str(len(items)))
        for item in items:
            jobListing = {}
            jobListing['title'] =  regex.sub("", item.title.text).strip()
            jobListing['pubdate'] = item.pubdate.text
            des=item.description.text.strip()
            soupDes = BeautifulSoup(des)
            pTags=soupDes.findAll('p')
            for pItem in pTags:
                res=pItem.get_text().split(':',1)
                label=res[0]
                val=res[1]
                jobListing[label]=val.strip()
                if label == 'View this Recruitment':
                    arr=val.split('#')
                    jobListing['jobId']=arr[1]
                aObj=pItem.find('a', href=True)
                if aObj!=None:
                    jobListing['link']=aObj['href']
            if 'location' not in jobListing.values():
                jobListing['location'] = site.location
            if 'state' not in jobListing.values():
                jobListing['state'] = site.state
            if 'Section' not in jobListing.values():
                jobListing['Section'] = db.sql.null()
            if site.descriptionRequired == 0:
                jobListing['description']= ''
            jobListings.append(jobListing)
        
        for jobListing in jobListings:
            session = Session()
            #2/9/2022 2:00:00 PM.
            #print(jobListing['title'], jobListing['Date Opened'])
            if(type(jobListing['Date Opened']) is not datetime):
                startDate=jobListing['Date Opened'].strip('.')
                try:
                    jobListing['Date Opened']=datetime.strptime(startDate, '%m/%d/%Y %H:%M:%S %p')
                except:
                    jobListing['Date Opened']=datetime.strptime(startDate, '%m/%d/%Y')                    
            #2/22/2022 11:59:00 PM
            if(jobListing['Close Date']=='Open Until Filled'):
                jobListing['Close Date']=db.sql.null()
            elif(type(jobListing['Close Date']) is not datetime):
                jobListing['Close Date']=datetime.strptime(jobListing['Close Date'].strip(), '%m/%d/%Y %H:%M:%S %p')
            #Tue, 12 Oct 2021 21:10:33 GMT
            if(type(jobListing['pubdate']) is not datetime):
                pubDate=jobListing['pubdate'].split(',')
                if(len(startDate)>1):
                    jobListing['pubdate']=datetime.strptime(pubDate[1].strip(), '%d %b %Y %H:%M:%S %Z').astimezone(pytz.UTC).replace(tzinfo=None)
                else:
                    jobListing['pubdate']=datetime.strptime(pubDate[0].strip(), '%d %b %Y %H:%M:%S %Z').astimezone(pytz.UTC).replace(tzinfo=None)
            #startDate, pubDate, closeDate, jobid, link, title, department, jobNumber, salaryRange, jobType, location, state, description):
            job = Job(jobListing['Date Opened'],jobListing['pubdate'],jobListing['Close Date'],int(jobListing['jobId'].replace("-","")),jobListing['link'],jobListing['title'],jobListing['Section'],jobListing['jobId'],jobListing['Salary'],jobListing['Employment Type'],jobListing['location'],jobListing['state'],db.sql.null())
            session.add(job)
            try:
                session.commit()
            except:
                session.rollback()

    


# %%



