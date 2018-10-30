# Fictitious News Database Reporting Tool


## Purpose of project
This project analyzes a fictitious news database. The questions it answers are:
1. Which of the articles are the three most popular?
2. Who are the most popular authors?
3. On which days were there more than 1% of HTTP request errors?


## Database Structure
This is a Postgresql data base containing three tables describing a fictitious 
news website. There are three tables: log, articles, and authors.

### Columns in the log table:
1. path
..* url path after the host name to the specified news article
2. ip
..* ip address to the website
3. method
..* the HTTP method used in this request
4. status
..* the HTTP status for this request
5. time
..* the time the request was made
6. id 
..* the unique id of this request

### Columns in the articles table:
1. author
..* the id of the author, which is the same as the id column in the authors table
2. title
..* the title of the article
3. slug 
..* the path extension of the article's url, which matches up with the path extension in the path column of the url table
4. lead
..* the introduction to the article
5. body 
..* the main body of the article
6. time
..* the time the article was submitted by the author
7. id
..* the unique id of the article 

### Columns in the authors table:
1. name
..* the name of the author 
2. bio
..* a short biography of the author
3. id
..* the author's unique id


## Necessary requirements to run this program:
1. Download the virtual machine. To download the virtual machine, Virtual Box in this case, go to virtualbox.org and download the correct version for your machine.

2. Download vagrant. Vagrant is used to configure the virtual machine. You can download it from vagrantup.com

3. Download the virtual machine configuration. You can download the GitHub repository
at https://github.com/udacity/fullstack-nanodegree-vm. 

4. Download the sql file. You can do so from this link: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
The file is called newsdata.sql.

5. Unzip the sql file, and put it it the vagrant directory which is shared with the virtual machine.

6. Change to your virtual machine sub directory within your command prompt. Once in that directory, change to the vagrant sub directory.

7. Load the sql database into your local database. To do so, type the command 'psql -d news -f newsdata.sql'.

5. Once in the vagrant subdirectory, run the command 'vagrant up' to initialize the virtual machine. 

6. Once the virtual machine is created, run 'vagrant ssh' to log into your machine.

7. Change into the /vagrant directory.

8. If you have created another directory with the sql and python file, change into that directory. 

9. Create the necessary views. Read below on how to do that.


## Views in SQL:
To create the necessary views, do the following.

1. Log into the virtual machine.

2. Change to the directory containing the sql file.

3. Run the command 'psql -d news' to connect to the sql database to be able to interact with it.

4. Run the command following commands:
                    
                    'create view article_views as
                    select split_part(path::text, '/', 3) as slug,
                    count(*) as num from log
                    group by path
                    order by num desc
                    offset 1
                    limit 8;'

                    'create view total_requests as 
                    select time::date, count(status) as requests from log
                    group by time::date;'

                    'create view request_errors as
                    select time::date, count(status) as errors from log
                    where status != '200 OK'
                    group by time::date;'


Once the views have been created, make sure you are in the correct directory with the python and sql files. You can run the python script by running the command 'python report_tool.py'. This will output the answers to the three questions stated above.