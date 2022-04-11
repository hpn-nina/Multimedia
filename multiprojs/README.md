# DBLP 

## Description
In this lab, we will try to go into and get one author listed in example.xml. From this author, we store their identity first in AUTHOR table. And then to the <r> tag which contain all the author's papers. In these, there will be co-author, where we need to store their name, key and pid in AUTHOR table too, alongside pid in another array for further exploration.
For each article/inproceedings/proceedings we will store it key in and array and when there is no more r tag, add these in AUTHOR_PAPERS as paper with author_id is author pid as tag.

In coauthor tag, there shall be many coauthors, add them to or AUTHOR table. There may be no need to go into their infos.

For further instruction or explaination, pls contact me @lialic.

**ALL COLUMNS** shall be name as *kebab-case*. For example: author-id, paper-id, ...

## GOTO 
[Number of tags in dblp](https://dblp.org/faq/How+are+data+annotations+used+in+dblp+xml.html)

[example.xml](https://dblp.org/pid/08/1510.xml)

[New update](https://blog.dblp.org/2020/08/18/new-dblp-url-scheme-and-api-changes/)

Pls download [XAMPP](https://www.apachefriends.org/index.html) and MYSQL Connector (using ```conda install -c anaconda mysql-connector-python```)

[Tutorial on parse XML file](https://www.geeksforgeeks.org/how-to-store-xml-data-into-a-mysql-database-using-python/)

[Data model](https://1drv.ms/u/s!AhZv8ipaWh2mgrdVHhTwJWOP0iklCw)


## Data model


```sql
CREATE TABLE authors (
	pid varchar(100) NOT NULL,
    name varchar(100) NOT NULL,
    n int,
    PRIMARY KEY (pid)
);

CREATE table papers (
	paper_key varchar(100) NOT NULL,
    title varchar(1000),
    authors JSON,
    year YEAR,
	another_infos JSON,
    PRIMARY KEY (paper_key)
);

CREATE table author_papers (
	pid varchar(100) NOT NULL,
    papers JSON,
    PRIMARY KEY (pid),
    CONSTRAINT FK_AuthorPapers FOREIGN KEY (pid)
    REFERENCES authors(pid)
);

CREATE table author_infos (
    pid varchar(100) NOT NULL PRIMARY KEY,
    awards JSON,
    others JSON,
    CONSTRAINT FK_AuthorsInfo FOREIGN KEY (pid)
    REFERENCES authors(pid)
);
```