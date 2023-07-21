import os
import subprocess


def run_docker_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing the command: {e}")
        return None

# Function to run Docker commands on each .sql file
def process_sql_file( sql_file_name):
    # Copy the SQL file to the container
    copy_command = f"docker cp OUTPUT/{sql_file_name}.sql mysql_56:/{sql_file_name}.sql"
    print(copy_command)
    run_docker_command(copy_command)

    # Execute MySQL commands in the container
    # Generally we use exec -it for interactive like entering password man
    command = (
       f"docker exec -it -e MYSQL_PWD=secret mysql_56 "
                f"mysql -uroot -e 'CREATE DATABASE {sql_file_name}; USE {sql_file_name}; SOURCE {sql_file_name}.sql;'"

    )
    run_docker_command(command)

# Get a list of all .sql files in the INPUT folder
input_folder = "./OUTPUT"
sql_files = [file for file in os.listdir(input_folder) if file.endswith(".sql")]


count=0
for file in sql_files:
    count+=1
    sql_file_name = file.rsplit('.',1)[0]
    sql_file_path = os.path.join(input_folder, file)
    if os.path.isfile(sql_file_path):
        process_sql_file( sql_file_name)
    else:
        print(f"File '{sql_file_path}' not found. Skipping...")
    print(f"✅ Running docker seeding - {file} :  ")

