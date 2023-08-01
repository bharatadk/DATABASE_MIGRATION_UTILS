# DATABASE_MIGRATION_UTILS
* step 1 : Parse sql statements and rewrite the input sql queries for tables in sorted correct order to avoid conflict ( python_script.py and python_rearrange.py).
* step 2 : Replace unwanted charatcters or url or words with new urls from the given list (replace_static_ur.py).
* step 3: Copy the .sql files from local to docker and seed all the databases in docker container (docker_mysql_phpmyadmin.py).
