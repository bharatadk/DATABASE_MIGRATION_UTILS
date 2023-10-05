# MySQL to PostgreSQL Conversion Guide

This document describes the steps and processes that were taken to convert a MySQL database to a PostgreSQL database for the HITE project. The conversion involved exporting the original MySQL file from the server, editing the SQL file, importing the updated SQL file to MySQL 5.6 in Docker, running the old project in Docker with MySQL, fixing and converting the data types, exporting the database in SQL format from phpMyAdmin, editing the SQL file again, creating a new database in pgAdmin, running the latest project with PostgreSQL, setting the database timezone to UTC, running the insert queries of the tables, and running the scripts to finalize the conversion.

✅ For our project we wrote some scripts using selenium,os,sqlparse modules to semi-automate our tasks.<br>
✅ We ran the scripts of OLD_HITE folder for old project and dumped mysql file and NEW_HITE_2021 project for new project.

## Export original MySQL file from server

The first step was to export the original MySQL file from the server using SSH. The command used was:

```bash
$ mysqldump -u root -p db_name > db_name.sql
```

where `db_name` is the name of the database.

## Edit the SQL file

The second step was to edit the SQL file using a text editor. The following changes were made:

- Replace `/var/www/websites` with `/mnt/gigenet_volume/websites`
- Replace `http://rmedia.4dlspace.com` static files with `https://rmedia.sfo3.digitaloceanspaces.com/public_html`
- Replace `https://rmedia.intelladapt.com` static files with `https://rmedia.sfo3.digitaloceanspaces.com/public_html`

## Import the updated SQL file to MySQL 5.6 in Docker

The third step was to import the updated SQL file to MySQL 5.6 in Docker. The commands used were:

```bash
$ docker cp db_name.sql mysql_56:/db_name.sql
$ docker exec -it mysql_56 mysql -uroot -p
Pwd: secret
mysql> CREATE DATABASE db_name;
USE db_name;
SOURCE db_name.sql;
exit
```

where `db_name` is the name of the database.

## Run the old project in Docker with MySQL

The fourth step was to run the old project in Docker with MySQL. The old project was located in the branch `old_hite`. The `.env` file was updated with `db_name`. The command used to run the project was:

```bash
$ docker-compose up -d
```

The project was accessible at http://0.0.0.0:70.

## Fix and convert the data types

The fifth step was to fix and convert the data types using a script that was accessible from the browser. The script was located at http://0.0.0.0:70/fix-index.php?link=1. The script fixed and converted the date, varbinary, blob, etc data types. The script was run three times with different parameters:

- http://0.0.0.0:70/fix-index.php?link=1
- http://0.0.0.0:70/fix-index.php?link=15
- http://0.0.0.0:70/fix-index.php?link=17

If successful, “Done 21” would be displayed on screen.

## Export this database in SQL format from phpMyAdmin

The sixth step was to export this database in SQL format from phpMyAdmin. phpMyAdmin was accessible at http://0.0.0.0:8080/. The export option was selected and the format was set to SQL.

Note: Exporting from terminal was not recommended as the field names were missing from insert query.

## Edit the SQL file again

The seventh step was to edit the SQL file again using a text editor. The following changes were made:

- Replace all \` with blank.
- Replace apostrophe (\\') with ('')
- Replace apostrophe (\\’) with (‘’)

## Create a new database in pgAdmin

The eighth step was to create a new database in pgAdmin using the same name as `db_name`.
The `.env` file was updated with `db_name`.

## Run the migration using following command:

```bash
$ vendor/bin/phinx migrate -e development
```

## Run the latest project with PostgreSQL

The project was accessible at http://0.0.0.0.

## Set database timezone to UTC

The tenth step was to set database timezone to UTC using pgAdmin or terminal. The command used was:

```sql
ALTER DATABASE db_name SET timezone TO 'UTC';
```

where `db_name` is the name of the database.

## The server PostgreSQL was restarted after this command.

```bash
$ sudo service postgresql restart
```

## Run the insert query of hite_users table

The eleventh step was to run the insert query of hite_users table using pgAdmin or terminal. The insert query was copied from the SQL file.

## Run the scripts to finalize the conversion

The twelfth and final step was to run the scripts to finalize the conversion using the browser. The scripts were located at http://0.0.0.0/fix-index.php?link=*. The scripts created new fields for the converted data, reinitialized primary keys, updated tables with datetime, and fixed other issues. The scripts were run in the following order:

- http://0.0.0.0/fix-index.php?link=a
- http://0.0.0.0/fix-index.php?link=1

Now insert all the other databases using commad \i source.sql. Finally run the last browser script.

- http://0.0.0.0/fix-index.php?link=2

If successful, “Done \*” would be displayed on screen.

## Steps to run

In old Mysql:

1. Copy/move the db you want to convert inside folder apostrophesavedsuccess/mysql1

2. Replace path in the database
   $ python OLD_HITE/replace_static_url.py

3. Copy the mysql file to docker
   $ python OLD_HITE/docker_mysql_create_and_store_databases.py

4. Convert data in mysql
   $ python OLD_HITE/docker_mysql_dump_sql_after_scripts.py

   - update database names in database_list[] array

5. Copy the downloaded file to need_to_remove_apostrophe folder. To remove quotes:
   $ python NEW_HITE_2021/replace_characters_apostrophe_tilde.py

6. Copy the sql file from need_to_remove_apostrophe folder to apostrophesavedsuccess folder. To extract only insert queries
   $ python NEW_HITE_2021/extract_insert_queries.py

7. To rearrange insert queries:
   $ python NEW_HITE_2021/rearrange_insert_queries.py

8. Rewrite insert query
   $ python NEW_HITE_2021/overwrite_insert_query.py

9. Go to pgadmin and create a new database

10. Open the latest hite project. Update env file with the new database name.
    Run the command in the terminal using phinx:
    $ vendor/bin/phinx migrate -e development

Then follow steps from:
https://docs.google.com/document/d/1Nj9U6OefzHfsycMff9FJEsl_atQkHV3BelG8g1CoxPc/edit#heading=h.nyaffl70hvh0
