"""
Import the updated sql file to mysql 5.6 in docker
$docker cp db_name.sql mysql_56:/db_name.sql
$docker exec -it mysql_56 mysql -uroot -p
Pwd: secret
mysql> CREATE DATABASE db_name;
USE db_name;
SOURCE db_name.sql;
exit

"""

import os
import subprocess

FILES_DIR = os.path.join(os.path.dirname(os.getcwd()), 'sqlfiles')

def run_docker_command(command):
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing the command: {e}")
        return None


def process_sql_file(sql_file_name):
    copy_command = f"docker cp {FILES_DIR}/mysql2/{sql_file_name}.sql mysql_56:/{sql_file_name}.sql"
    print(copy_command)
    run_docker_command(copy_command)

    # Execute MySQL commands in the container
    command = (
        f"docker exec -it -e MYSQL_PWD=secret mysql_56 "
        f"mysql -u root -e 'CREATE DATABASE {sql_file_name}; USE {sql_file_name}; SOURCE {sql_file_name}.sql;'"
    )
    run_docker_command(command)


# Get a list of all .sql files in the INPUT folder
input_folder = os.path.join(FILES_DIR,"mysql2")
sql_files = [file for file in os.listdir(
    input_folder) if file.endswith(".sql")]


count = 0
for file in sql_files:
    count += 1
    sql_file_name = file.rsplit(".", 1)[0]
    sql_file_path = os.path.join(input_folder, file)
    if os.path.isfile(sql_file_path):
        process_sql_file(sql_file_name)
    else:
        print(f"File '{sql_file_path}' not found. Skipping...")
    print(f"✅ Running docker seeding - {file} :  ")
