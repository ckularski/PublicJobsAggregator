CREATE TABLE 'jobs' (
  'jobid' bigint NOT NULL,
  'link' varchar(200) NOT NULL,
  'title' varchar(300) DEFAULT NULL,
  'department' varchar(100) DEFAULT NULL,
  'jobNumber' varchar(50) DEFAULT NULL,
  'salaryRange' varchar(100) DEFAULT NULL,
  'jobType' varchar(50) DEFAULT NULL,
  'location' varchar(100) DEFAULT NULL,
  'state' varchar(25) DEFAULT NULL,
  'description' text,
  'startDate' datetime DEFAULT NULL,
  'pubDate' datetime DEFAULT NULL,
  'closeDate' datetime DEFAULT NULL,
  PRIMARY KEY ('jobid','link')
);