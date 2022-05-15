delete from jobs where closeDate is not null and datediff(NOW(), closeDate)>0;
delete from jobs where closeDate is null and datediff(NOW(), pubDate)>90;
