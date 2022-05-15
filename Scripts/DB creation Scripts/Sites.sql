CREATE TABLE 'sites' (
  'link' varchar(200) NOT NULL,
  'title' varchar(50) DEFAULT NULL,
  'location' varchar(50) DEFAULT NULL,
  'codeBase' varchar(10) DEFAULT NULL,
  'state' varchar(50) DEFAULT NULL,
  'descriptionRequired' tinyint(1) DEFAULT '0',
  PRIMARY KEY ('link')
)